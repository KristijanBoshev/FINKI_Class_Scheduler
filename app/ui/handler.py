from app.data.sample_data import subjects_data
import streamlit as st
from app.core.scheduling_system import SchedulingSystem


def handle_schedule_change(scheduling_system: SchedulingSystem):
    st.subheader("Modify Schedule")
    change_type = st.radio("Select alternative:", ["professor", "classroom"])

    # If the change type is "professor"
    if change_type == "professor":
        subject = st.selectbox("Select subject:", [sub['name'] for sub in subjects_data])

        # Select the current professor from those available for the subject
        all_professors = scheduling_system.get_all_professors_for_subject(subject)
        current_professor = st.selectbox("Select current professor:", all_professors)

        # Select lesson type (theoretical or practical)
        lesson_type = st.selectbox("Select lesson type:", ["Theoretical", "Practical"])

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
        subjects = [sub['name'] for sub in subjects_data]
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