import sys
import os

# Add the project root directory (parent directory of `app`) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scheduling_system import SchedulingSystem
from app.utils.helpers import determine_change_type


def run_scheduling_system():
    scheduling_system = SchedulingSystem()
    scheduling_system.initialize_base_schedule()

    while True:
        if scheduling_system.is_end_of_week():
            scheduling_system.start_new_week()
            print("Starting a new week. Schedule reset to base configuration.")

        user_query = input("Enter your query in natural language or 'quit' to exit: ")
        if user_query.lower() == 'quit':
            break

        if user_query.lower() in ['show schedule', 'current schedule']:
            schedule = scheduling_system.current_week_schedule

            for entry in schedule:
                subject = entry['subject']
                lesson_type = entry['lesson_type']
                classroom = entry['classroom']
                professor = entry['professor']

                for time_slot in entry['time_slots']:
                    print(f"{subject} - {lesson_type} - {classroom} - {professor} - {time_slot}")

        change_type = determine_change_type(user_query)
        if change_type is None:
            print("Unable to determine if you're asking about a classroom or professor change. Please clarify your query.")
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

                    # Get the slots for the selected professor (if the change type is professor)
                    if change_type == 'professor':
                        subject_type = scheduling_system.get_subject_type(result['subject'])
                        slots = scheduling_system.get_all_slots_for_professor(new_value, result['subject'], subject_type)
                        print(f"Time slots for {new_value} teaching {result['subject']} ({subject_type}): {slots}")

                        # Allow the user to select the specific slot to update
                        slot_choice = input(f"Selectt a time slot from the above list {new_value}: ")
                        if slot_choice in slots:
                            day, time = slot_choice.split()

                            # Update the schedule with the selected professor and time slot
                            if scheduling_system.update_schedule(result['subject'], day, time, change_type, new_value):
                                print(f"Schedule updated. New {change_type} for {result['subject']} on {day} at {time}: {new_value}")
                            else:
                                print("Failed to update the schedule. Please try again.")
                        else:
                            print("Invalid time slot selected.")
                    else:
                        # For classroom change, just update directly
                        day = result['day']
                        time = result['time']
                        if scheduling_system.update_schedule(result['subject'], day, time, change_type, new_value):
                            print(f"Schedule updated. New {change_type} for {result['subject']} on {day} at {time}: {new_value}")
                        else:
                            print("Failed to update the schedule. Please try again.")
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print(f"No suitable alternatives found for {change_type}. Schedule remains unchanged.")

# Run the scheduling system
if __name__ == "__main__":
    run_scheduling_system()