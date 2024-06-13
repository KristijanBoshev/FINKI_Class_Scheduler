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
    {"name": "VNP", "times_per_week_theoretical": 4, "times_per_week_practical": 4, "theoretical_duration": 3,
     "practical_duration": 2, "year_of_listening": 3},
    {"name": "OS", "times_per_week_theoretical": 6, "times_per_week_practical": 6, "theoretical_duration": 2,
     "practical_duration": 2, "year_of_listening": 3},
    {"name": "E-Vlada", "times_per_week_theoretical": 1, "times_per_week_practical": 0, "theoretical_duration": 3,
     "practical_duration": 0, "year_of_listening": 1}
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
                         "Fri 4pm", "Fri 5pm", "Fri 6pm", "Fri 7pm"]}
]

# Define professors and their availability
professors = [
    {"name": "Prof. Smith", "subjects": ["VNP"], "unavailable_slots": ["Mon 8am", "Tue 9am"]},
    {"name": "Prof. Johnson", "subjects": ["OS", "E-Vlada"], "unavailable_slots": ["Wed 10am", "Thu 11am", "Fri 12pm"]},
    {"name": "Prof. Lee", "subjects": ["VNP", "OS"], "unavailable_slots": ["Mon 10am", "Tue 2pm", "Wed 11am"]},
    {"name": "Prof. Brown", "subjects": ["VNP"], "unavailable_slots": ["Thu 1pm", "Fri 3pm"]},
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
            day, hour = unavailable_slot.split()
            professor_hour_schedule[professor["name"]][(day, hour)] = True

    for subject in subjects_sorted:
        year_of_listening = subject["year_of_listening"]
        times_per_week_theoretical = subject["times_per_week_theoretical"]
        times_per_week_practical = subject["times_per_week_practical"]
        for lesson_type, duration, times in [
            ("Theoretical", subject["theoretical_duration"], times_per_week_theoretical),
            ("Practical", subject["practical_duration"], times_per_week_practical)]:
            for _ in range(times):
                slot_assigned = False
                for professor in state["professors"]:
                    if subject["name"] not in professor["subjects"]:
                        continue
                    for classroom in state["classrooms"]:
                        for start_index in range(0, len(classroom["available_slots"])):
                            available_slot_subset = classroom["available_slots"][start_index:start_index + duration]
                            if len(available_slot_subset) < duration:
                                continue

                            conflict = False
                            for time_slot in available_slot_subset:
                                day, hour = time_slot.split()
                                if (hour_year_schedule[(day, hour)][year_of_listening] or
                                        classroom_hour_schedule[classroom["name"]][(day, hour)] or
                                        professor_hour_schedule[professor["name"]][(day, hour)]):
                                    conflict = True
                                    break

                            if conflict:
                                continue

                            if len(available_slot_subset) == duration:
                                slot_assigned = True
                                for slot in available_slot_subset:
                                    day, hour = slot.split()
                                    hour_year_schedule[(day, hour)][year_of_listening] = True
                                    classroom_hour_schedule[classroom["name"]][(day, hour)] = True
                                    professor_hour_schedule[professor["name"]][(day, hour)] = True
                                schedule.append(
                                    {"subject": subject["name"], "lesson_type": lesson_type,
                                     "classroom": classroom["name"],
                                     "professor": professor["name"], "slots": available_slot_subset})
                                break
                        if slot_assigned:
                            break
                    if slot_assigned:
                        break

    return {"schedule": schedule}


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
        f"{item['subject']} - {item['lesson_type']} - {item['classroom']} - {item['professor']} - {', '.join(item['slots'])}")