import Class_Managment_System as cms
from datetime import timedelta, datetime
from Tasks import *
from crewai import Crew

class SchedulingSystem:
    def __init__(self):
        self.base_schedule = None
        self.current_week_schedule = None
        self.week_start_date = None

    def initialize_base_schedule(self):
        final_state = cms.runnable.invoke({})
        self.base_schedule = final_state["schedule"]
        self.start_new_week()

    def start_new_week(self):
        self.week_start_date = datetime.now().date() - timedelta(days=datetime.now().weekday())
        self.current_week_schedule = self.base_schedule.copy()

    def update_schedule(self, subject, time, change_type, new_value):
        for class_item in self.current_week_schedule:
            if class_item['subject'] == subject and time in class_item['time_slots']:
                if change_type == 'classroom':
                    class_item['classroom'] = new_value
                elif change_type == 'professor':
                    class_item['professor'] = new_value
                return True
        return False

    def get_class_info(self, subject, time):
        for class_item in self.current_week_schedule:
            if class_item['subject'] == subject and time in class_item['time_slots']:
                return class_item
        return None

    def is_end_of_week(self):
        current_date = datetime.now().date()
        return current_date >= self.week_start_date + timedelta(days=7)

    def get_available_professors(self, subject):
        available_professors = []
        for professor in cms.professors:
            if subject in professor["subjects"]:
                available_professors.append(professor["name"])
        return available_professors

    def get_available_classrooms(self, time):
        available_classrooms = []
        for classroom in cms.classrooms:
            if time in classroom["available_slots"]:
                available_classrooms.append(classroom["name"])
        return available_classrooms

# Initialize the scheduling system
scheduling_system = SchedulingSystem()
scheduling_system.initialize_base_schedule()

def process_query(query, change_type):
    context = f"""
    Current week schedule: {scheduling_system.current_week_schedule}
    Query: {query}
    Change Type: {change_type}
    Based on the current schedule and the specified change type, provide a response in the following format:
    subject: [subject name]
    time: [time of the class]
    current_value: [current professor/classroom name]
    """
    response = llm.invoke(context)
    return response.content

def parse_llm_response(response_content):
    print("LLM Response:", response_content)
    lines = response_content.strip().split('\n')
    parsed_response = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            parsed_response[key.strip()] = value.strip()
        else:
            print(f"Skipping line as it does not contain a key-value pair: '{line}'")
    return parsed_response

scheduling_crew = Crew(
    agents=[classroom_substitution_agent, professor_substitution_agent, schedule_manager_agent],
    tasks=[suggest_classroom_substitution, suggest_professor_substitution, manage_schedule_changes],
    llm=llm,
    verbose=2
)

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
            print("Unable to determine if you're asking about a classroom or professor change. Please clarify your query.")
            continue

        response_content = process_query(user_query, change_type)

        try:
            parsed_response = parse_llm_response(response_content)
            subject = parsed_response['subject']
            time = parsed_response['time']
            current_value = parsed_response['current_value']
        except KeyError as e:
            print(f"Couldn't parse the query correctly. Missing key: {e}. Please try again.")
            continue

        # Prepare the context based on the type of change
        context = f"Subject: {subject}, Time: {time}, Current Value: {current_value}"

        result = None
        if change_type == "professor":
            available_professors = scheduling_system.get_available_professors(subject)
            context += f", Available Professors: {', '.join(available_professors)}"

            # Activate the relevant specialist by setting up the correct crew_inputs
            crew_inputs = {
                "change_type": change_type,
                "context": context,
            }
            result = scheduling_crew.kickoff(crew_inputs)

        elif change_type == "classroom":
            available_classrooms = scheduling_system.get_available_classrooms(time)
            context += f", Available Classrooms: {', '.join(available_classrooms)}"

            # Activate the relevant specialist by setting up the correct crew_inputs
            crew_inputs = {
                "change_type": change_type,
                "context": context,
            }
            result = scheduling_crew.kickoff(crew_inputs)

        # Update the schedule based on the result
        try:
            new_value = extract_new_value(result, change_type)
            if new_value:
                scheduling_system.update_schedule(subject, time, change_type, new_value)
                print(f"Schedule updated. New {change_type} for {subject} on {time}: {new_value}")
            else:
                print(f"No suitable alternative {change_type} found. Schedule remains unchanged.")
        except ValueError as e:
            print(e)

    print("System exiting. The current week's schedule has been updated based on approved changes.")

def extract_new_value(result, change_type):
    for task in result.tasks_output:
        if change_type == "professor" and "Suggested professor" in task.raw:
            return task.raw.split("Suggested professor: ")[-1].split(".")[0].strip()
        elif change_type == "classroom" and "Suggested classroom" in task.raw:
            return task.raw.split("Suggested classroom: ")[-1].split(".")[0].strip()

    # If no suitable substitution is found, raise an error or handle accordingly
    raise ValueError(f"No suitable alternative {change_type} found. Schedule remains unchanged.")

# Run the scheduling system
if __name__ == "__main__":
    run_scheduling_system()