import networkx as nx
import matplotlib.pyplot as plt
from typing import TypedDict, Annotated, List
import operator

"""
Define the SchedulingState dictionary structure, it contains key-value pairs, each of the values is represented
as a list of another set dictionaries for the appropriate subject,classroom,schedule
This is the crucial part for our Langgraph app to work
"""

class SchedulingState(TypedDict):
    subjects: Annotated[List[dict], operator.add]
    classrooms: Annotated[List[dict], operator.add]
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
                         "Fri 4pm", "Fri 5pm", "Fri 6pm", "Fri 7pm"]},
]


# Define nodes, returns the value of the specific key
def add_subjects(state):
    return {"subjects": subjects}


def add_classrooms(state):
    return {"classrooms": classrooms}


# Scheduling algorithm
def schedule_classes(state):
    # Empty list to store the final report
    schedule = []
    # I created sorted descending list of subjects based on the maximum duration,
    # In this way the subjects with longer duration will be stored first, which is good due to breakdown of one lesson in different days
    subjects_sorted = sorted(state["subjects"], key=lambda x: max(x["theoretical_duration"], x["practical_duration"]),
                             reverse=True)

    # This dictionary helps keep track of which year_of_listening has already scheduled a subject on a specific hour of the day
    hour_year_schedule = {(day, hour): {j: False for j in range(1, 5)} for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]
                          for hour in
                          ["8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"]}
    # Keeping track of which classroom has already scheduled a subject on a specific hour of the day
    classroom_hour_schedule = {
        classroom["name"]: {(day, hour): False for day in ["Mon", "Tue", "Wed", "Thu", "Fri"] for hour in
                            ["8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"]} for
        classroom in state["classrooms"]}
    # Iterates over each subject in the list
    for subject in subjects_sorted:
        year_of_listening = subject["year_of_listening"]
        times_per_week_theoretical = subject["times_per_week_theoretical"]
        times_per_week_practical = subject["times_per_week_practical"]
        # This loop iterates over two tuples
        # Each tuple contains the lesson type, duration, and number of times per week.
        for lesson_type, duration, times in [
            ("Theoretical", subject["theoretical_duration"], times_per_week_theoretical),
            ("Practical", subject["practical_duration"], times_per_week_practical)]:
            # How many times per week do we have
            for _ in range(times):
                # Flag to check if slot has been assigned for the current subject and type
                slot_assigned = False
                # Iterating over each classroom
                for classroom in state["classrooms"]:
                    # Checking available slots in the current classroom
                    for start_index in range(0, len(classroom["available_slots"])):
                        # Checking if there is enough free space for the whole duration
                        available_slot_subset = classroom["available_slots"][start_index:start_index + duration]
                        # If there is not space, go to the next iteration
                        if len(available_slot_subset) < duration:
                            continue

                        # Check if there is a time conflict with another subject from the same year_of_listening
                        conflict = False
                        for time_slot in available_slot_subset:
                            # Extracting day and hour
                            day, hour = time_slot.split()
                            # if there is another subject from the same year in the same hour of the day,->conflict
                            if hour_year_schedule[(day, hour)][year_of_listening] or classroom_hour_schedule[classroom["name"]][(day, hour)]:
                                conflict = True
                                break
                        # Go next iteration if there is conflict
                        if conflict:
                            continue

                        # If no conflict, mark the slots as assigned
                        if len(available_slot_subset) == duration:
                            slot_assigned = True
                            for slot in available_slot_subset:
                                day, hour = slot.split()
                                hour_year_schedule[(day, hour)][year_of_listening] = True
                                classroom_hour_schedule[classroom["name"]][(day, hour)] = True
                            schedule.append(
                                {"subject": subject["name"], "lesson_type": lesson_type, "classroom": classroom["name"],
                                 "slots": available_slot_subset})
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
graph.add_node("schedule_classes", schedule_classes)
# Add edges
graph.add_edge("add_subjects", "add_classrooms")
graph.add_edge("add_classrooms", "schedule_classes")
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
    print(f"{item['subject']} - {item['lesson_type']} - {item['classroom']} - {', '.join(item['slots'])}")
