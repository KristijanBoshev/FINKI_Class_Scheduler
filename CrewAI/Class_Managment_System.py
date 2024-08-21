import networkx as nx
import matplotlib.pyplot as plt
from typing import TypedDict, Annotated, List
import operator
import random


# Define the SchedulingState dictionary structure
class SchedulingState(TypedDict):
    subjects: Annotated[List[dict], operator.add]
    classrooms: Annotated[List[dict], operator.add]
    professors: Annotated[List[dict], operator.add]
    schedule: Annotated[List[dict], operator.add]


# Dummy data
# Define subject and classroom details
subjects = [
    {"name": "VNP", "times_per_week_theoretical": 7, "times_per_week_practical": 6, "theoretical_duration": 3,
     "practical_duration": 2, "year_of_listening": 3},
    {"name": "OS", "times_per_week_theoretical": 6, "times_per_week_practical": 6, "theoretical_duration": 2,
     "practical_duration": 2, "year_of_listening": 2},
    {"name": "E-Vlada", "times_per_week_theoretical": 1, "times_per_week_practical": 0, "theoretical_duration": 3,
     "practical_duration": 0, "year_of_listening": 2},
    {"name": "SP", "times_per_week_theoretical": 5, "times_per_week_practical": 5, "theoretical_duration": 2,
     "practical_duration": 2, "year_of_listening": 1},
    {"name": "DS", "times_per_week_theoretical": 5, "times_per_week_practical": 5, "theoretical_duration": 3,
     "practical_duration": 3, "year_of_listening": 1},
    {"name": "Pretpriemnistvo", "times_per_week_theoretical": 8, "times_per_week_practical": 8,
     "theoretical_duration": 2,
     "practical_duration": 1, "year_of_listening": 4},

]

classrooms = [
    {"name": "138",
     "available_slots": ["Mon 8am", "Mon 9am", "Mon 10am", "Mon 11am", "Mon 12pm", "Mon 1pm", "Mon 2pm", "Mon 3pm",
                         "Mon 4pm", "Mon 5pm", "Mon 6pm", "Mon 7pm",
                         "Tue 8am", "Tue 9am", "Tue 10am", "Tue 11am", "Tue 12pm", "Tue 1pm", "Tue 2pm", "Tue 3pm",
                         "Tue 4pm", "Tue 5pm", "Tue 6pm", "Tue 7pm",
                         "Wed 8am", "Wed 9am", "Wed 10am", "Wed 11am", "Wed 12pm", "Wed 1pm", "Wed 2pm", "Wed 3pm",
                         "Wed 4pm", "Wed 5pm", "Wed 6pm", "Wed 7pm",
                         "Thu 8am", "Thu 9am", "Thu 10am", "Thu 11am", "Thu 12pm", "Thu 1pm", "Thu 2pm", "Thu 3pm",
                         "Thu 4pm", "Thu 5pm", "Thu 6pm", "Thu 7pm",
                         "Fri 8am", "Fri 9am", "Fri 10am", "Fri 11am", "Fri 12pm", "Fri 1pm", "Fri 2pm", "Fri 3pm",
                         "Fri 4pm", "Fri 5pm", "Fri 6pm", "Fri 7pm"]},
    {"name": "215",
     "available_slots": ["Mon 8am", "Mon 9am", "Mon 10am", "Mon 11am", "Mon 12pm", "Mon 1pm", "Mon 2pm", "Mon 3pm",
                         "Mon 4pm", "Mon 5pm", "Mon 6pm", "Mon 7pm",
                         "Tue 8am", "Tue 9am", "Tue 10am", "Tue 11am", "Tue 12pm", "Tue 1pm", "Tue 2pm", "Tue 3pm",
                         "Tue 4pm", "Tue 5pm", "Tue 6pm", "Tue 7pm",
                         "Wed 8am", "Wed 9am", "Wed 10am", "Wed 11am", "Wed 12pm", "Wed 1pm", "Wed 2pm", "Wed 3pm",
                         "Wed 4pm", "Wed 5pm", "Wed 6pm", "Wed 7pm",
                         "Thu 8am", "Thu 9am", "Thu 10am", "Thu 11am", "Thu 12pm", "Thu 1pm", "Thu 2pm", "Thu 3pm",
                         "Thu 4pm", "Thu 5pm", "Thu 6pm", "Thu 7pm",
                         "Fri 8am", "Fri 9am", "Fri 10am", "Fri 11am", "Fri 12pm", "Fri 1pm", "Fri 2pm", "Fri 3pm",
                         "Fri 4pm", "Fri 5pm", "Fri 6pm", "Fri 7pm"]},
{"name": "13",
     "available_slots": ["Mon 8am", "Mon 9am", "Mon 10am", "Mon 11am", "Mon 12pm", "Mon 1pm", "Mon 2pm", "Mon 3pm",
                         "Mon 4pm", "Mon 5pm", "Mon 6pm", "Mon 7pm",
                         "Tue 8am", "Tue 9am", "Tue 10am", "Tue 11am", "Tue 12pm", "Tue 1pm", "Tue 2pm", "Tue 3pm",
                         "Tue 4pm", "Tue 5pm", "Tue 6pm", "Tue 7pm",
                         "Wed 8am", "Wed 9am", "Wed 10am", "Wed 11am", "Wed 12pm", "Wed 1pm", "Wed 2pm", "Wed 3pm",
                         "Wed 4pm", "Wed 5pm", "Wed 6pm", "Wed 7pm",
                         "Thu 8am", "Thu 9am", "Thu 10am", "Thu 11am", "Thu 12pm", "Thu 1pm", "Thu 2pm", "Thu 3pm",
                         "Thu 4pm", "Thu 5pm", "Thu 6pm", "Thu 7pm",
                         "Fri 8am", "Fri 9am", "Fri 10am", "Fri 11am", "Fri 12pm", "Fri 1pm", "Fri 2pm", "Fri 3pm",
                         "Fri 4pm", "Fri 5pm", "Fri 6pm", "Fri 7pm"]}
]

# Define professors and their availability
professors = [
    {"name": "Prof. Igor", "subjects": ["VNP", "OS", "OOP"], "unavailable_slots": ["Mon", "Tue 9am"]},
    {"name": "Prof. Riste", "subjects": ["OS", "E-Vlada", "OOP"],
     "unavailable_slots": ["Tue 7pm", "Wed 10am", "Thu 11am", "Fri 12pm"]},
    {"name": "Prof. Andrea", "subjects": ["VNP", "OS", "DS"], "unavailable_slots": ["Mon 10am", "Tue 2pm", "Wed 11am"]},
    {"name": "Prof. Mile", "subjects": ["VNP", "OOP", "SP"], "unavailable_slots": ["Thu 1pm", "Fri 3pm"]},
    {"name": "Prof. Ilinka", "subjects": ["VNP", "DS", "Pretpriemnistvo"], "unavailable_slots": ["Fri 9am", "Fri 4pm"]},
]


# Define nodes, returns the value of the specific key
def add_subjects(state):
    return {"subjects": subjects}


def add_classrooms(state):
    return {"classrooms": classrooms}


def add_professors(state):
    return {"professors": professors}


# Scheduling algorithm

def schedule_classes(state):
    random.seed(42)

    schedule = []

    subjects_sorted = sorted(state["subjects"], key=lambda x: max(x["theoretical_duration"], x["practical_duration"]),
                             reverse=True)

    hour_year_schedule = {(day, hour): {j: False for j in range(1, 5)} for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]
                          for hour in
                          ["8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"]}

    classroom_hour_schedule = {
        classroom["name"]: {(day, hour): False for day in ["Mon", "Tue", "Wed", "Thu", "Fri"] for hour in
                            ["8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"]} for
        classroom in state["classrooms"]}

    professor_hour_schedule = {
        professor["name"]: {(day, hour): False for day in ["Mon", "Tue", "Wed", "Thu", "Fri"] for hour in
                            ["8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"]} for
        professor in state["professors"]}

    for professor in state["professors"]:
        for unavailable_slot in professor["unavailable_slots"]:
            parts = unavailable_slot.split()
            day = parts[0]
            if len(parts) > 1:
                hour = parts[1]
                professor_hour_schedule[professor["name"]][(day, hour)] = True
            else:
                for hour in ["8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"]:
                    professor_hour_schedule[professor["name"]][(day, hour)] = True

    subject_professor_assignment = {subject["name"]: {"Theoretical": 0, "Practical": 0} for subject in subjects_sorted}

    def assign_initial_classes(lesson_type, subject, professors, duration):
        for professor in professors:
            for classroom in state["classrooms"]:
                for start_index in range(0, len(classroom["available_slots"])):
                    available_slot_subset = classroom["available_slots"][start_index:start_index + duration]
                    if len(available_slot_subset) < duration:
                        continue

                    conflict = False
                    for time_slot in available_slot_subset:
                        day, hour = time_slot.split()
                        if (hour_year_schedule[(day, hour)][subject["year_of_listening"]] or
                                classroom_hour_schedule[classroom["name"]][(day, hour)] or
                                professor_hour_schedule[professor["name"]][(day, hour)]):
                            conflict = True
                            break

                    if conflict:
                        continue

                    if len(available_slot_subset) == duration:
                        for slot in available_slot_subset:
                            day, hour = slot.split()
                            hour_year_schedule[(day, hour)][subject["year_of_listening"]] = True
                            classroom_hour_schedule[classroom["name"]][(day, hour)] = True
                            professor_hour_schedule[professor["name"]][(day, hour)] = True
                        schedule.append({
                            "subject": subject["name"],
                            "lesson_type": lesson_type,
                            "classroom": classroom["name"],
                            "professor": professor["name"],
                            "time_slots": available_slot_subset
                        })
                        subject_professor_assignment[subject["name"]][lesson_type] += 1
                        return True
        return False

    def assign_remaining_slots(lesson_type, duration, times, subject):
        assigned_count = subject_professor_assignment[subject["name"]][lesson_type]
        while assigned_count < times:
            slot_assigned = False

            eligible_professors = [prof for prof in state["professors"] if subject["name"] in prof["subjects"]]

            eligible_professors.sort(key=lambda x: (len(x["subjects"]), x["name"]))

            for professor in eligible_professors:
                if slot_assigned:
                    break
                sorted_classrooms = sorted(state["classrooms"], key=lambda x: x["name"])
                for classroom in sorted_classrooms:
                    for start_index in range(0, len(classroom["available_slots"])):
                        available_slot_subset = classroom["available_slots"][start_index:start_index + duration]
                        if len(available_slot_subset) < duration:
                            continue

                        conflict = False
                        for time_slot in available_slot_subset:
                            day, hour = time_slot.split()
                            if (hour_year_schedule[(day, hour)][subject["year_of_listening"]] or
                                    classroom_hour_schedule[classroom["name"]][(day, hour)] or
                                    professor_hour_schedule[professor["name"]][(day, hour)]):
                                conflict = True
                                break

                        if conflict:
                            continue

                        if len(available_slot_subset) == duration:
                            slot_assigned = True
                            assigned_count += 1
                            for slot in available_slot_subset:
                                day, hour = slot.split()
                                hour_year_schedule[(day, hour)][subject["year_of_listening"]] = True
                                classroom_hour_schedule[classroom["name"]][(day, hour)] = True
                                professor_hour_schedule[professor["name"]][(day, hour)] = True
                            schedule.append({
                                "subject": subject["name"],
                                "lesson_type": lesson_type,
                                "classroom": classroom["name"],
                                "professor": professor["name"],
                                "time_slots": available_slot_subset
                            })
                            subject_professor_assignment[subject["name"]][lesson_type] += 1
                            break

                    if slot_assigned:
                        break
                if slot_assigned:
                    break

            if not slot_assigned:
                break  # Exit if no more slots can be assigned to avoid infinite loop

        return assigned_count

    for subject in subjects_sorted:
        times_per_week_theoretical = subject["times_per_week_theoretical"]
        times_per_week_practical = subject["times_per_week_practical"]
        duration_theoretical = subject["theoretical_duration"]
        duration_practical = subject["practical_duration"]

        professors_for_subject = [prof for prof in state["professors"] if subject["name"] in prof["subjects"]]

        for professor in professors_for_subject:
            if subject_professor_assignment[subject["name"]]["Theoretical"] < times_per_week_theoretical:
                if not assign_initial_classes("Theoretical", subject, [professor], duration_theoretical):
                    print(f"Unable to assign theoretical class for {subject['name']} with {professor['name']}")
            if subject_professor_assignment[subject["name"]]["Practical"] < times_per_week_practical:
                if not assign_initial_classes("Practical", subject, [professor], duration_practical):
                    print(f"Unable to assign practical class for {subject['name']} with {professor['name']}")

        # Assign remaining theoretical classes
        total_assigned_theoretical = assign_remaining_slots("Theoretical", duration_theoretical,
                                                            times_per_week_theoretical, subject)
        if total_assigned_theoretical < times_per_week_theoretical:
            print(f"Unable to fully assign theoretical classes for {subject['name']}")

        # Assign remaining practical classes
        total_assigned_practical = assign_remaining_slots("Practical", duration_practical, times_per_week_practical,
                                                          subject)
        if total_assigned_practical < times_per_week_practical:
            print(f"Unable to fully assign practical classes for {subject['name']}")

    # Remove entries with missing time slots from the final schedule
    final_schedule = [entry for entry in schedule if entry["time_slots"]]

    return {"schedule": final_schedule}


# Create the graph
from langgraph.graph import StateGraph, END

# Instance of StateGraph for our predefined SchedulingState structure
graph = StateGraph(SchedulingState)
# Add nodes
graph.add_node("add_subjects", add_subjects)
graph.add_node("add_classrooms", add_classrooms)
graph.add_node("add_professors", add_professors)
graph.add_node("schedule_classes", schedule_classes)
# Add edges
graph.add_edge("add_subjects", "add_classrooms")
graph.add_edge("add_classrooms", "add_professors")
graph.add_edge("add_professors", "schedule_classes")
graph.add_edge("schedule_classes", END)

graph.set_entry_point("add_subjects")

# Visualize the graph using NetworkX
G = nx.DiGraph()
for node in graph.nodes:
    G.add_node(node)
for edge in graph.edges:
    G.add_edge(edge[0], edge[1])

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
plt.show()

# Run the graph
runnable = graph.compile()
# Generated state from the graph
final_state = runnable.invoke({})

# Print the schedule
print("Class Schedule:")
for item in final_state["schedule"]:
    print(
        f"{item['subject']} - {item['lesson_type']} - {item['classroom']} - {item['professor']} - {', '.join(item['time_slots'])}")
