import random


def schedule_classes(state):
    random.seed(42)

    schedule = []

    subjects_sorted = sorted(state["subjects"], key=lambda x: max(x["theoretical_duration"], x["practical_duration"]),
                             reverse=True)

    hour_year_schedule = {(day, hour): {j: False for j in range(1, 5)} for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]
                          for hour in
                          ["8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"]}

    classroom_hour_schedule = {
        classroom["name"]: {(day, hour): False for day in ["Mon", "Tue", "Wed", "Thu", "Fri"] for hour in
                            ["8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"]} for
        classroom in state["classrooms"]}

    professor_hour_schedule = {
        professor["name"]: {(day, hour): False for day in ["Mon", "Tue", "Wed", "Thu", "Fri"] for hour in
                            ["8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"]} for
        professor in state["professors"]}

    for professor in state["professors"]:
        for unavailable_slot in professor["unavailable_slots"]:
            parts = unavailable_slot.split()
            day = parts[0]
            if len(parts) > 1:
                hour = parts[1]
                professor_hour_schedule[professor["name"]][(day, hour)] = True
            else:
                for hour in ["8am", "9am", "10am", "11am", "12pm", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm"]:
                    professor_hour_schedule[professor["name"]][(day, hour)] = True

    subject_professor_assignment = {subject["name"]: {"Theoretical": 0, "Practical": 0} for subject in subjects_sorted}

    def assign_initial_classes(lesson_type, subject, professors, duration):
        for professor in professors:
            for classroom in state["classrooms"]:
                for start_index in range(0, len(classroom["available_slots"])):
                    available_slot_subset = classroom["available_slots"][start_index:start_index + duration]
                    if len(available_slot_subset) < duration:
                        continue

                    conflict = False
                    for time_slot in available_slot_subset:
                        day, hour = time_slot.split()
                        if (hour_year_schedule[(day, hour)][subject["year_of_listening"]] or
                                classroom_hour_schedule[classroom["name"]][(day, hour)] or
                                professor_hour_schedule[professor["name"]][(day, hour)]):
                            conflict = True
                            break

                    if conflict:
                        continue

                    if len(available_slot_subset) == duration:
                        for slot in available_slot_subset:
                            day, hour = slot.split()
                            hour_year_schedule[(day, hour)][subject["year_of_listening"]] = True
                            classroom_hour_schedule[classroom["name"]][(day, hour)] = True
                            professor_hour_schedule[professor["name"]][(day, hour)] = True
                        schedule.append({
                            "subject": subject["name"],
                            "lesson_type": lesson_type,
                            "classroom": classroom["name"],
                            "professor": professor["name"],
                            "time_slots": available_slot_subset
                        })
                        subject_professor_assignment[subject["name"]][lesson_type] += 1
                        return True
        return False

    def assign_remaining_slots(lesson_type, duration, times, subject):
        assigned_count = subject_professor_assignment[subject["name"]][lesson_type]
        while assigned_count < times:
            slot_assigned = False

            eligible_professors = [prof for prof in state["professors"] if subject["name"] in prof["subjects"]]

            eligible_professors.sort(key=lambda x: (len(x["subjects"]), x["name"]))

            for professor in eligible_professors:
                if slot_assigned:
                    break
                sorted_classrooms = sorted(state["classrooms"], key=lambda x: x["name"])
                for classroom in sorted_classrooms:
                    for start_index in range(0, len(classroom["available_slots"])):
                        available_slot_subset = classroom["available_slots"][start_index:start_index + duration]
                        if len(available_slot_subset) < duration:
                            continue

                        conflict = False
                        for time_slot in available_slot_subset:
                            day, hour = time_slot.split()
                            if (hour_year_schedule[(day, hour)][subject["year_of_listening"]] or
                                    classroom_hour_schedule[classroom["name"]][(day, hour)] or
                                    professor_hour_schedule[professor["name"]][(day, hour)]):
                                conflict = True
                                break

                        if conflict:
                            continue

                        if len(available_slot_subset) == duration:
                            slot_assigned = True
                            assigned_count += 1
                            for slot in available_slot_subset:
                                day, hour = slot.split()
                                hour_year_schedule[(day, hour)][subject["year_of_listening"]] = True
                                classroom_hour_schedule[classroom["name"]][(day, hour)] = True
                                professor_hour_schedule[professor["name"]][(day, hour)] = True
                            schedule.append({
                                "subject": subject["name"],
                                "lesson_type": lesson_type,
                                "classroom": classroom["name"],
                                "professor": professor["name"],
                                "time_slots": available_slot_subset
                            })
                            subject_professor_assignment[subject["name"]][lesson_type] += 1
                            break

                    if slot_assigned:
                        break
                if slot_assigned:
                    break

            if not slot_assigned:
                break  # Exit if no more slots can be assigned to avoid infinite loop

        return assigned_count

    for subject in subjects_sorted:
        times_per_week_theoretical = subject["times_per_week_theoretical"]
        times_per_week_practical = subject["times_per_week_practical"]
        duration_theoretical = subject["theoretical_duration"]
        duration_practical = subject["practical_duration"]

        professors_for_subject = [prof for prof in state["professors"] if subject["name"] in prof["subjects"]]

        for professor in professors_for_subject:
            if subject_professor_assignment[subject["name"]]["Theoretical"] < times_per_week_theoretical:
                if not assign_initial_classes("Theoretical", subject, [professor], duration_theoretical):
                    print(f"Unable to assign theoretical class for {subject['name']} with {professor['name']}")
            if subject_professor_assignment[subject["name"]]["Practical"] < times_per_week_practical:
                if not assign_initial_classes("Practical", subject, [professor], duration_practical):
                    print(f"Unable to assign practical class for {subject['name']} with {professor['name']}")

        # Assign remaining theoretical classes
        total_assigned_theoretical = assign_remaining_slots("Theoretical", duration_theoretical,
                                                            times_per_week_theoretical, subject)
        if total_assigned_theoretical < times_per_week_theoretical:
            print(f"Unable to fully assign theoretical classes for {subject['name']}")

        # Assign remaining practical classes
        total_assigned_practical = assign_remaining_slots("Practical", duration_practical, times_per_week_practical,
                                                          subject)
        if total_assigned_practical < times_per_week_practical:
            print(f"Unable to fully assign practical classes for {subject['name']}")

    # Remove entries with missing time slots from the final schedule
    final_schedule = [entry for entry in schedule if entry["time_slots"]]

    return {"schedule": final_schedule}