def determine_change_type(query: str) -> str:
    query = query.lower()
    if 'classroom' in query or 'room' in query:
        return 'classroom'
    elif 'professor' in query or 'teacher' in query or 'lecturer' in query:
        return 'professor'
    else:
        return None