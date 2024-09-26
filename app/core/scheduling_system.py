from langgraph.graph import StateGraph, END
from datetime import datetime, timedelta
from app.state.state_graph import run_graph
from app.state.main_state import MainState
from app.data.sample_data import subjects_data, professors_data, classrooms_data
from typing import List



class SchedulingSystem:
    def __init__(self):
        self.base_schedule = None
        self.current_week_schedule = None
        self.week_start_date = None
        self.graph = self.create_graph()

    def create_graph(self):
        graph = StateGraph(MainState)

        graph.add_node("process_query", self.process_query)
        graph.add_node("find_alternatives", self.find_alternatives)

        graph.add_edge("process_query", "find_alternatives")
        graph.add_edge("find_alternatives", END)

        graph.set_entry_point("process_query")

        return graph.compile()

    def initialize_base_schedule(self):
        final_state = run_graph()
        self.base_schedule = final_state["schedule"]
        self.start_new_week()

    def start_new_week(self):
        self.week_start_date = datetime.now().date() - timedelta(days=datetime.now().weekday())
        self.current_week_schedule = self.base_schedule.copy()

    def is_end_of_week(self):
        current_date = datetime.now().date()
        return current_date >= self.week_start_date + timedelta(days=7)

    def process_query(self, state: MainState):
        query = state['query']
        change_type = state['change_type']

        # Simple parsing of the query
        words = query.lower().split()
        subject = next((word for word in words if word in [sub['name'].lower() for sub in subjects_data]), None)
        day = next((word for word in words if
                    word.lower() in ["monday", "tuesday", "wednesday", "thursday", "friday", "mon", "tue", "wed", "thu",
                                     "fri"]), None)
        time = next((word for word in words if "am" in word or "pm" in word), None)

        if day:
            day = day[:3].capitalize()  # Normalize to Mon, Tue, Wed, etc.

        state['subject'] = subject
        state['day'] = day
        state['time'] = time

        return state

    def find_alternatives(self, state: MainState):
        change_type = state['change_type']
        subject = state['subject']
        day = state['day']
        time = state['time']
        current_professor = self.get_current_professor(subject, day)
        current_classroom = self.get_current_classroom(subject, day, time)

        alternatives = []
        if subject:
            if change_type == "professor":
                subject_type = self.get_subject_type(subject)  # New method to get the subject type
                all_professors = self.get_all_professors_for_subject(subject, exclude_professor=current_professor)
                recommended_professors = self.recommend_professors_based_on_subject_type(all_professors, subject_type)
                alternatives = recommended_professors
            elif change_type == "classroom":
                time_slots = self.get_time_slots_for_subject(subject, day)
                all_available_classrooms = self.get_available_classrooms_for_slots(time_slots)
                alternatives = [classroom for classroom in all_available_classrooms if classroom != current_classroom]

        state['alternatives'] = alternatives
        return state

    def get_subject_type(self, subject: str) -> str:
        """Determine if the subject is theoretical or practical."""
        for sub in subjects_data:
            if sub['name'].lower() == subject.lower():
                return sub.get('type', 'theoretical')  # Assuming default type is 'theoretical'
        return 'theoretical'

    def recommend_professors_based_on_subject_type(self, professors: List[str], subject_type: str) -> List[str]:
        """Recommend professors who can teach a particular type of subject."""
        recommended_professors = []
        for prof in professors:
            prof_data = next((p for p in professors_data if p['name'] == prof), None)
            if prof_data and subject_type in prof_data.get('subject_types', ['theoretical']):
                recommended_professors.append(prof)
        return recommended_professors


    def get_current_professor(self, subject, time):
        current_professor = None
        for class_item in self.current_week_schedule:
            if class_item['subject'].lower() == subject.lower():
                current_professor = class_item['professor']
                break
        return current_professor

    def get_all_slots_for_professor(self, professor, subject, subject_type):
        slots = []
        for class_item in self.current_week_schedule:
            # Match on subject, professor, and subject type
            if (class_item['subject'].lower() == subject.lower() and
                    class_item['professor'].lower() == professor.lower()):

                class_type = class_item.get('lesson_type', '').lower()  # Use 'lesson_type' key instead
                if class_type == subject_type.lower():
                    slots.extend(class_item['time_slots'])

        return slots

    def get_all_professors_for_subject(self, subject: str, exclude_professor: str = None) -> List[str]:
        """Get all professors for a given subject, excluding the current professor."""
        professors = [prof["name"] for prof in professors_data if
                      subject.lower() in [s.lower() for s in prof["subjects"]]]
        if exclude_professor:
            professors = [prof for prof in professors if prof != exclude_professor]
        return professors

    def get_current_classroom(self, subject, day, time):
        for class_item in self.current_week_schedule:
            if class_item['subject'].lower() == subject.lower():
                for slot in class_item['time_slots']:
                    if slot.startswith(f"{day} {time}"):
                        return class_item['classroom']
        return None

    def get_time_slots_for_subject(self, subject, day):
        for class_item in self.current_week_schedule:
            if class_item['subject'].lower() == subject.lower():
                if day:
                    return [slot for slot in class_item['time_slots'] if slot.startswith(day)]
                else:
                    return class_item['time_slots']
        return []

    def is_classroom_available_for_slots(self, classroom, time_slots):
        for class_item in self.current_week_schedule:
            if class_item['classroom'] == classroom:
                # Check if any time slots overlap with the required time slots
                for slot in time_slots:
                    if any(existing_slot.startswith(slot) for existing_slot in class_item['time_slots']):
                        return False
        return True

    def get_available_classrooms_for_slots(self, time_slots):
        available_classrooms = []
        for classroom in classrooms_data:
            if self.is_classroom_available_for_slots(classroom['name'], time_slots):
                available_classrooms.append(classroom['name'])
        return available_classrooms

    def update_schedule(self, subject, day, time, change_type, new_value):
        updated = False
        for class_item in self.current_week_schedule:
            if class_item['subject'].lower() == subject.lower():
                # Check if the time slot matches
                matching_slots = [slot for slot in class_item['time_slots'] if slot.startswith(f"{day} {time}")]
                if matching_slots:
                    if change_type == 'professor':
                        class_item['professor'] = new_value
                    elif change_type == 'classroom':
                        class_item['classroom'] = new_value
                    updated = True
                    break  # Once updated, break the loop since the correct class was found
        return updated

    def get_schedule_changes(self):
        changes = []
        for base, current in zip(self.base_schedule, self.current_week_schedule):
            if base != current:
                changes.append(f"Changed {current['subject']}: Professor {base['professor']} -> {current['professor']}, Classroom {base['classroom']} -> {current['classroom']}")
        return changes

    def run_query(self, query: str, change_type: str) -> dict:
        initial_state = MainState(
            subjects=subjects_data,
            classrooms=classrooms_data,
            professors=professors_data,
            schedule=self.current_week_schedule,
            query=query,
            change_type=change_type,
            context="",
            alternatives=[],
            subject="",
            day="",
            time=""
        )
        final_state = self.graph.invoke(initial_state)
        return final_state