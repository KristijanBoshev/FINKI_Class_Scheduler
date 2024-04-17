import networkx as nx
import matplotlib.pyplot as plt
from typing import TypedDict, Annotated, List
import operator


# Define the state structure
class SchedulingState(TypedDict):
    subjects: Annotated[List[dict], operator.add]
    classrooms: Annotated[List[dict], operator.add]
    schedule: Annotated[List[dict], operator.add]


# Define subject and classroom details
subjects = [
    {"name": "VNP", "times_per_week_theoretical": 1, "times_per_week_practical": 1, "theoretical_duration": 3,
     "practical_duration": 2},
    {"name": "OS", "times_per_week_theoretical": 2, "times_per_week_practical": 1, "theoretical_duration": 2,
     "practical_duration": 3},
    {"name": "E-Vlada", "times_per_week_theoretical": 2, "times_per_week_practical": 0, "theoretical_duration": 2,
     "practical_duration": 0}
]

classrooms = [
    {"name": "Room A",
     "available_slots": ["Mon 9am", "Mon 10am", "Mon 11am", "Tue 2pm", "Tue 3pm", "Tue 4pm", "Wed 11am", "Wed 12pm",
                         "Wed 1pm", "Thu 3pm", "Thu 4pm", "Thu 5pm", "Fri 10am", "Fri 11am", "Fri 12pm"]},
    {"name": "Room B",
     "available_slots": ["Mon 10am", "Mon 11am", "Mon 12pm", "Tue 1pm", "Tue 2pm", "Tue 3pm", "Wed 3pm", "Wed 4pm",
                         "Wed 5pm", "Thu 9am", "Thu 10am", "Thu 11am", "Fri 11am", "Fri 12pm", "Fri 1pm"]}
]


# Define nodes
def add_subjects(state):
    return {"subjects": subjects}


def add_classrooms(state):
    return {"classrooms": classrooms}


def schedule_classes(state):
    schedule = []
    subjects_sorted = sorted(state["subjects"], key=lambda x: max(x["theoretical_duration"], x["practical_duration"]),
                             reverse=True)

    for subject in subjects_sorted:
        times_per_week_theoretical = subject["times_per_week_theoretical"]
        times_per_week_practical = subject["times_per_week_practical"]

        for lesson_type, duration, times in [
            ("Theoretical", subject["theoretical_duration"], times_per_week_theoretical),
            ("Practical", subject["practical_duration"], times_per_week_practical)]:
            for _ in range(times):
                for classroom in state["classrooms"]:
                    available_slots = [slot for slot in classroom["available_slots"][:duration]]
                    if len(available_slots) == duration:
                        for slot in available_slots:
                            classroom["available_slots"].remove(slot)
                        schedule.append(
                            {"subject": subject["name"], "classroom": classroom["name"], "slots": available_slots,
                             "lesson_type": lesson_type})
                        break

    return {"schedule": schedule}


# Create the graph
from langgraph.graph import StateGraph, END

graph = StateGraph(SchedulingState)
graph.add_node("add_subjects", add_subjects)
graph.add_node("add_classrooms", add_classrooms)
graph.add_node("schedule_classes", schedule_classes)

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
final_state = runnable.invoke({})

# Print the schedule
print("Class Schedule:")
for item in final_state["schedule"]:
    print(f"{item['subject']} - {item['lesson_type']} - {item['classroom']} - {', '.join(item['slots'])}")
