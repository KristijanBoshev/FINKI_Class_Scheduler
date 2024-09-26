import os
import sys

# Add the project root directory (parent directory of `app`) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scheduling_system import SchedulingSystem
import streamlit as st
from ui.handler import handle_schedule_change

@st.cache_resource
def initialize_scheduling_system():
    if 'scheduling_system' not in st.session_state:
        scheduling_system = SchedulingSystem()
        scheduling_system.initialize_base_schedule()
        st.session_state.scheduling_system = scheduling_system
    return st.session_state.scheduling_system


scheduling_system = initialize_scheduling_system()


def display_base_schedule():
    st.subheader("Base Schedule (Static)")
    schedule = scheduling_system.base_schedule  # Unchanged base schedule
    if schedule:
        for entry in schedule:
            subject = entry['subject']
            lesson_type = entry['lesson_type']
            classroom = entry['classroom']
            professor = entry['professor']
            for time_slot in entry['time_slots']:
                st.write(f"{subject} - {lesson_type} - {classroom} - {professor} - {time_slot}")
    else:
        st.write("No base schedule available.")


# Function to display the current week's schedule (modifiable)
def display_current_schedule():
    st.subheader("Current Schedule (Dynamic)")
    schedule = scheduling_system.current_week_schedule
    if schedule:
        for entry in schedule:
            subject = entry['subject']
            lesson_type = entry['lesson_type']
            classroom = entry['classroom']
            professor = entry['professor']
            for time_slot in entry['time_slots']:
                st.write(f"{subject} - {lesson_type} - {classroom} - {professor} - {time_slot}")
    else:
        st.write("No current schedule available.")

    # Display changes
    changes = scheduling_system.get_schedule_changes()
    if changes:
        st.subheader("Changes made:")
        for change in changes:
            st.write(change)


# Main app layout with 3 tabs: Base Schedule, Change Schedule, and Current Schedule
tab1, tab2, tab3 = st.tabs(["Base Schedule", "Modify Schedule", "Current Schedule"])

# Tab 1: Display the base schedule
with tab1:
    display_base_schedule()

# Tab 2: Allow the user to modify the schedule
with tab2:
    handle_schedule_change(scheduling_system)

# Tab 3: Display the current (updated) schedule
with tab3:
    display_current_schedule()

if scheduling_system.is_end_of_week():
    if st.button("Start New Week"):
        scheduling_system.start_new_week()
        st.success("New week started! Schedule reset to base configuration.")
