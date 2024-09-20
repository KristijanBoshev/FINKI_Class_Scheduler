import streamlit as st
import Class_Managment_System as cms
from Crew import SchedulingSystem


# Initialize the scheduling system (Cache the instance to persist across app sessions)
@st.cache_resource
def initialize_scheduling_system():
    if 'scheduling_system' not in st.session_state:
        scheduling_system = SchedulingSystem()
        scheduling_system.initialize_base_schedule()
        st.session_state.scheduling_system = scheduling_system
    return st.session_state.scheduling_system


scheduling_system = initialize_scheduling_system()


# Function to display the base schedule (unchanged)
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

# Function to handle schedule changes
def handle_schedule_change():
    st.subheader("Modify Schedule")
    change_type = st.radio("Select alternative:", ["professor", "classroom"])

    # If the change type is "professor"
    if change_type == "professor":
        subject = st.selectbox("Select subject:", [sub['name'] for sub in cms.subjects])

        # Select the current professor from those available for the subject
        all_professors = scheduling_system.get_all_professors_for_subject(subject)
        current_professor = st.selectbox("Select current professor:", all_professors)

        # Select lesson type (theoretical or practical)
        lesson_type = st.selectbox("Select lesson type:", ["theoretical", "practical"])

        # Show other available professors for the same subject excluding the current professor
        available_professors = [prof for prof in all_professors if prof != current_professor]

        if available_professors:
            # Choose the new professor to change to
            selected_professor = st.selectbox("Select new professor:", available_professors)

            # Display available time slots for the new professor
            available_time_slots = scheduling_system.get_all_slots_for_professor(selected_professor, subject, lesson_type)
            selected_time_slot = st.selectbox("Select new time slot:", available_time_slots)

            # Confirm and update the schedule
            if st.button("Confirm Change"):
                day, time = selected_time_slot.split()  # Assuming format "Day Time"
                if scheduling_system.update_schedule(subject, day, time, change_type, selected_professor):
                    st.success(f"Schedule updated! New professor for {subject} ({lesson_type}) at {selected_time_slot}: {selected_professor}")
                else:
                    st.error("Failed to update the schedule. Please try again.")
        else:
            st.warning("No other professors available for this subject.")

    # If the change type is "classroom"
    else:  # Classroom change
        subjects = [sub['name'] for sub in cms.subjects]
        subject = st.selectbox("Select subject:", subjects, key="classroom_subject_select")
        day = st.selectbox("Select day:", ["Mon", "Tue", "Wed", "Thu", "Fri"], key="classroom_day_select")
        time = st.selectbox("Select time:",
                            ["8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"],
                            key="classroom_time_select")

        # Automatically generate the alternatives for classrooms
        query = f"Change {change_type} for {subject} on {day} at {time}"
        result = scheduling_system.run_query(query, change_type)

        if result['alternatives']:
            st.write(f"Available alternatives for {change_type}:")
            choice = st.selectbox("Choose an alternative:", result['alternatives'],
                                  key="classroom_alternative_select")

            st.write(f"Selected Alternative: {choice}")

            # Directly update the schedule without needing to press "Find Alternatives"
            if st.button("Confirm Change", key="confirm_classroom_change"):
                update_successful = scheduling_system.update_schedule(subject, day, time, change_type, choice)

                st.write(f"Update Status: {update_successful}")

                if update_successful:
                    st.success(f"Schedule updated! New {change_type} for {subject} on {day} at {time}: {choice}")
                    st.session_state.schedule_updated = True  # Track the update
                else:
                    st.error("Failed to update the schedule. Please try again.")
        else:
            st.warning(f"No suitable alternatives found for {change_type}. Schedule remains unchanged.")


# Main app layout with 3 tabs: Base Schedule, Change Schedule, and Current Schedule
tab1, tab2, tab3 = st.tabs(["Base Schedule", "Modify Schedule", "Current Schedule"])

# Tab 1: Display the base schedule
with tab1:
    display_base_schedule()

# Tab 2: Allow the user to modify the schedule
with tab2:
    handle_schedule_change()

# Tab 3: Display the current (updated) schedule
with tab3:
    display_current_schedule()

if scheduling_system.is_end_of_week():
    if st.button("Start New Week"):
        scheduling_system.start_new_week()
        st.success("New week started! Schedule reset to base configuration.")

