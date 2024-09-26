from langgraph.graph import StateGraph, END
from .scheduling_state import SchedulingState
from app.core.assign import schedule_classes
from app.data.sample_data import *

def add_subjects(state):
    return {"subjects": subjects_data}


def add_classrooms(state):
    return {"classrooms": classrooms_data}


def add_professors(state):
    return {"professors": professors_data}

def run_graph():
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

    # Run the graph
    runnable = graph.compile()
    # Generated state from the graph
    final_state = runnable.invoke({})

    print("Class Schedule:")
    for item in final_state["schedule"]:
        print(
            f"{item['subject']} - {item['lesson_type']} - {item['classroom']} - {item['professor']} - {', '.join(item['time_slots'])}")
    return final_state

