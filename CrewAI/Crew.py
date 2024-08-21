import Class_Managment_System as cms
from datetime import timedelta, datetime
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator


class SchedulingState(TypedDict):
    subjects: Annotated[List[dict], operator.add]
    classrooms: Annotated[List[dict], operator.add]
    professors: Annotated[List[dict], operator.add]
    schedule: Annotated[List[dict], operator.add]
    query: str
    change_type: str
    context: str
    alternatives: List[str]
    subject: str
    time: str


class SchedulingSystem:
    def __init__(self):
        self.base_schedule = None
        self.current_week_schedule = None
        self.week_start_date = None
        self.graph = self.create_graph()

    def create_graph(self):
        graph = StateGraph(SchedulingState)

        graph.add_node("process_query", self.process_query)
        graph.add_node("find_alternatives", self.find_alternatives)

        graph.add_edge("process_query", "find_alternatives")
        graph.add_edge("find_alternatives", END)

        graph.set_entry_point("process_query")

        return graph.compile()

    def initialize_base_schedule(self):
        final_state = cms.runnable.invoke({})
        self.base_schedule = final_state["schedule"]
        self.start_new_week()

    def start_new_week(self):
        self.week_start_date = datetime.now().date() - timedelta(days=datetime.now().weekday())
        self.current_week_schedule = self.base_schedule.copy()

    def is_end_of_week(self):
        current_date = datetime.now().date()
        return current_date >= self.week_start_date + timedelta(days=7)

    def process_query(self, state: SchedulingState) -> SchedulingState:
        query = state['query']
        change_type = state['change_type']

        # Simple parsing of the query
        words = query.lower().split()
        subject = next((word for word in words if word in [sub['name'].lower() for sub in cms.subjects]), None)
        time = next((word for word in words if word in ["monday", "tuesday", "wednesday", "thursday", "friday"]), None)

        state['subject'] = subject
        state['time'] = time

        return state

    def find_alternatives(self, state: SchedulingState) -> SchedulingState:
        change_type = state['change_type']
        subject = state['subject']
        time = state['time']
        current_professor = self.get_current_professor(subject, time)
        current_classroom = self.get_current_classroom(subject, time)

        alternatives = []
        if subject:
            if change_type == "professor":
                all_professors = self.get_all_professors_for_subject(subject)
                alternatives = [prof for prof in all_professors if prof != current_professor]
            elif change_type == "classroom":
                all_available_classrooms = self.get_available_classrooms_for_time()
                alternatives = [classroom for classroom in all_available_classrooms if classroom != current_classroom]
                if not alternatives:
                    alternatives = [classroom['name'] for classroom in cms.classrooms if
                                    classroom['name'] != current_classroom and self.is_classroom_available(
                                        classroom['name'])]

        state['alternatives'] = alternatives
        return state

    def get_current_professor(self, subject, time):
        current_professor = None
        for class_item in self.current_week_schedule:
            if class_item['subject'].lower() == subject.lower():
                current_professor = class_item['professor']
                break
        return current_professor

    def get_all_slots_for_professor(self, professor, subject):
        slots = []
        for class_item in self.current_week_schedule:
            if class_item['subject'].lower() == subject.lower() and class_item['professor'] == professor:
                slots.extend(class_item['time_slots'])
        return slots

    def get_all_professors_for_subject(self, subject):
        return [prof["name"] for prof in cms.professors if subject.lower() in [s.lower() for s in prof["subjects"]]]

    def get_current_classroom(self, subject, time):
        for class_item in self.current_week_schedule:
            if class_item['subject'].lower() == subject.lower() and time in class_item['time_slots']:
                return class_item['classroom']
        return None

    def get_available_classrooms_for_time(self):
        available_classrooms = []
        for classroom in cms.classrooms:
            if self.is_classroom_available(classroom['name']):
                available_classrooms.append(classroom['name'])
        return available_classrooms

    def is_classroom_available(self, classroom):
        for class_item in self.current_week_schedule:
            if class_item['classroom'] == classroom:
                return False
        return True

    def update_schedule(self, subject, time, change_type, new_value):
        for class_item in self.current_week_schedule:
            if class_item['subject'].lower() == subject.lower() and (not time or time in class_item['time_slots']):
                if change_type == 'professor':
                    class_item['professor'] = new_value
                elif change_type == 'classroom':
                    class_item['classroom'] = new_value
                return True
        return False

    def run_query(self, query: str, change_type: str) -> dict:
        initial_state = SchedulingState(
            subjects=cms.subjects,
            classrooms=cms.classrooms,
            professors=cms.professors,
            schedule=self.current_week_schedule,
            query=query,
            change_type=change_type,
            context="",
            alternatives=[],
            subject="",
            time=""
        )
        final_state = self.graph.invoke(initial_state)
        return final_state


# Initialize the scheduling system
scheduling_system = SchedulingSystem()
scheduling_system.initialize_base_schedule()


def determine_change_type(query):
    query = query.lower()
    if 'classroom' in query or 'room' in query:
        return 'classroom'
    elif 'professor' in query or 'teacher' in query or 'lecturer' in query:
        return 'professor'
    else:
        return None


def run_scheduling_system():
    while True:
        if scheduling_system.is_end_of_week():
            scheduling_system.start_new_week()
            print("Starting a new week. Schedule reset to base configuration.")

        user_query = input("Enter your query in natural language or 'quit' to exit: ")
        if user_query.lower() == 'quit':
            break

        change_type = determine_change_type(user_query)
        if change_type is None:
            print(
                "Unable to determine if you're asking about a classroom or professor change. Please clarify your query.")
            continue

        result = scheduling_system.run_query(user_query, change_type)

        if result['alternatives']:
            print(f"Possible alternatives for {change_type}:")
            for i, alt in enumerate(result['alternatives'], 1):
                print(f"{i}. {alt}")

            choice = input("Enter the number of your choice or 'cancel' to abort: ")
            if choice.lower() == 'cancel':
                continue

            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(result['alternatives']):
                    new_value = result['alternatives'][choice_index]

                    # Get all slots for the chosen professor
                    all_slots = scheduling_system.get_all_slots_for_professor(new_value, result['subject'])
                    print(f"Available slots for {new_value} to teach {result['subject']}:")
                    for slot in all_slots:
                        print(f"- {slot}")

                    final_choice = input("Enter the time slot you want to assign or 'cancel' to abort: ")
                    if final_choice.lower() == 'cancel':
                        continue

                    if scheduling_system.update_schedule(result['subject'], final_choice, change_type, new_value):
                        print(
                            f"Schedule updated. New {change_type} for {result['subject']} at {final_choice}: {new_value}")
                    else:
                        print("Failed to update the schedule. Please try again.")
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print(f"No suitable alternatives found for {change_type}. Schedule remains unchanged.")

    print("System exiting. The current week's schedule has been updated based on approved changes.")


# Run the scheduling system
if __name__ == "__main__":
    run_scheduling_system()