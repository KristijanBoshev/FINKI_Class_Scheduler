from .scheduling_state import SchedulingState
from typing import List

class MainState(SchedulingState):
    query: str
    change_type: str
    context: str
    alternatives: List[str]
    subject: str
    day: str
    time: str