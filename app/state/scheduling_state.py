from typing import TypedDict, Annotated, List
import operator

class SchedulingState(TypedDict):
    subjects: Annotated[List[dict], operator.add]
    classrooms: Annotated[List[dict], operator.add]
    professors: Annotated[List[dict], operator.add]
    schedule: Annotated[List[dict], operator.add]