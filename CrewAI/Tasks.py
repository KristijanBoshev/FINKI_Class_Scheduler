from crewai import Task
from Agents import *

suggest_classroom_substitution = Task(
    description="Suggest a substitute classroom for a given time slot.",
    agent=classroom_substitution_agent,
    expected_output="A string containing the suggested classroom and the reason for suggestion"
)

suggest_professor_substitution = Task(
    description="Suggest a substitute professor for a given subject and time slot.",
    agent=professor_substitution_agent,
    expected_output="A string containing the suggested professor and the reason for suggestion"
)

manage_schedule_changes = Task(
    description="Manage scheduling changes, suggesting appropriate substitutions as needed.",
    agent=schedule_manager_agent,
    expected_output="A detailed string describing the schedule changes and substitutions made"
)

