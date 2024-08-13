import Class_Managment_System as cms
from datetime import timedelta,datetime
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
                if change_type == 'subject':
                    class_item['subject'] = new_value
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
        return current_date.weekday() == 4 and datetime.now().hour >= 20

scheduling_system = SchedulingSystem()
scheduling_system.initialize_base_schedule()

def run_scheduling_system():
    # Initialize tasks
    task_subject_substitution = suggest_subject_substitution
    task_professor_substitution = suggest_professor_substitution
    task_manage_schedule_changes = manage_schedule_changes

    # Initialize crew with tasks
    scheduling_crew = Crew(
        agents=[subject_substitution_agent, professor_substitution_agent, schedule_manager_agent],
        tasks=[task_subject_substitution, task_professor_substitution, task_manage_schedule_changes],
        verbose=2  # Increase this for more detailed output
    )

    while True:
        if scheduling_system.is_end_of_week():
            scheduling_system.start_new_week()
            print("Starting a new week. Schedule reset to base configuration.")

        user_query = input("Enter your query (change_type, subject, time, current_value) or 'quit' to exit: ")
        if user_query.lower() == 'quit':
            break

        parts = user_query.split(',')
        if len(parts) < 4:
            print("Invalid query format. Please use: change_type (subject/professor), subject, time, current_value")
            continue

        change_type, subject, time, current_value = [part.strip() for part in parts]

        # Dynamically create the task based on user input
        if change_type == "subject":
            task = task_subject_substitution(subject, time, current_value)
        elif change_type == "professor":
            task = task_professor_substitution(subject, time, current_value)
        else:
            print("Invalid change type. Please specify 'subject' or 'professor'.")
            continue

        # Execute the task using Crew
        result = scheduling_crew.kickoff(inputs={"change_type": change_type, "subject": subject, "time": time, "current_value": current_value})

        print(result)

    print("System exiting. The current week's schedule has been updated based on approved changes.")

# Run the scheduling system
if __name__ == "__main__":
    run_scheduling_system()
