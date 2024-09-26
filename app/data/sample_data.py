from typing import List, Dict

# Dummy data
# Define subject and classroom details
subjects_data = [
    {"name": "VNP", "times_per_week_theoretical": 7, "times_per_week_practical": 6, "theoretical_duration": 3,
     "practical_duration": 2, "year_of_listening": 3},
    {"name": "OS", "times_per_week_theoretical": 6, "times_per_week_practical": 6, "theoretical_duration": 2,
     "practical_duration": 2, "year_of_listening": 2},
    {"name": "E-Vlada", "times_per_week_theoretical": 1, "times_per_week_practical": 0, "theoretical_duration": 3,
     "practical_duration": 0, "year_of_listening": 2},
    {"name": "SP", "times_per_week_theoretical": 5, "times_per_week_practical": 5, "theoretical_duration": 2,
     "practical_duration": 2, "year_of_listening": 1},
    {"name": "DS", "times_per_week_theoretical": 5, "times_per_week_practical": 5, "theoretical_duration": 3,
     "practical_duration": 3, "year_of_listening": 1},
    {"name": "Pretpriemnistvo", "times_per_week_theoretical": 8, "times_per_week_practical": 8,
     "theoretical_duration": 2,
     "practical_duration": 1, "year_of_listening": 4},

]

classrooms_data = [
    {"name": "138",
     "available_slots": ["Mon 8am", "Mon 9am", "Mon 10am", "Mon 11am", "Mon 12pm", "Mon 1pm", "Mon 2pm", "Mon 3pm",
                         "Mon 4pm", "Mon 5pm", "Mon 6pm", "Mon 7pm",
                         "Tue 8am", "Tue 9am", "Tue 10am", "Tue 11am", "Tue 12pm", "Tue 1pm", "Tue 2pm", "Tue 3pm",
                         "Tue 4pm", "Tue 5pm", "Tue 6pm", "Tue 7pm",
                         "Wed 8am", "Wed 9am", "Wed 10am", "Wed 11am", "Wed 12pm", "Wed 1pm", "Wed 2pm", "Wed 3pm",
                         "Wed 4pm", "Wed 5pm", "Wed 6pm", "Wed 7pm",
                         "Thu 8am", "Thu 9am", "Thu 10am", "Thu 11am", "Thu 12pm", "Thu 1pm", "Thu 2pm", "Thu 3pm",
                         "Thu 4pm", "Thu 5pm", "Thu 6pm", "Thu 7pm",
                         "Fri 8am", "Fri 9am", "Fri 10am", "Fri 11am", "Fri 12pm", "Fri 1pm", "Fri 2pm", "Fri 3pm",
                         "Fri 4pm", "Fri 5pm", "Fri 6pm", "Fri 7pm"]},
    {"name": "215",
     "available_slots": ["Mon 8am", "Mon 9am", "Mon 10am", "Mon 11am", "Mon 12pm", "Mon 1pm", "Mon 2pm", "Mon 3pm",
                         "Mon 4pm", "Mon 5pm", "Mon 6pm", "Mon 7pm",
                         "Tue 8am", "Tue 9am", "Tue 10am", "Tue 11am", "Tue 12pm", "Tue 1pm", "Tue 2pm", "Tue 3pm",
                         "Tue 4pm", "Tue 5pm", "Tue 6pm", "Tue 7pm",
                         "Wed 8am", "Wed 9am", "Wed 10am", "Wed 11am", "Wed 12pm", "Wed 1pm", "Wed 2pm", "Wed 3pm",
                         "Wed 4pm", "Wed 5pm", "Wed 6pm", "Wed 7pm",
                         "Thu 8am", "Thu 9am", "Thu 10am", "Thu 11am", "Thu 12pm", "Thu 1pm", "Thu 2pm", "Thu 3pm",
                         "Thu 4pm", "Thu 5pm", "Thu 6pm", "Thu 7pm",
                         "Fri 8am", "Fri 9am", "Fri 10am", "Fri 11am", "Fri 12pm", "Fri 1pm", "Fri 2pm", "Fri 3pm",
                         "Fri 4pm", "Fri 5pm", "Fri 6pm", "Fri 7pm"]},
    {"name": "13",
     "available_slots": ["Mon 8am", "Mon 9am", "Mon 10am", "Mon 11am", "Mon 12pm", "Mon 1pm", "Mon 2pm", "Mon 3pm",
                         "Mon 4pm", "Mon 5pm", "Mon 6pm", "Mon 7pm",
                         "Tue 8am", "Tue 9am", "Tue 10am", "Tue 11am", "Tue 12pm", "Tue 1pm", "Tue 2pm", "Tue 3pm",
                         "Tue 4pm", "Tue 5pm", "Tue 6pm", "Tue 7pm",
                         "Wed 8am", "Wed 9am", "Wed 10am", "Wed 11am", "Wed 12pm", "Wed 1pm", "Wed 2pm", "Wed 3pm",
                         "Wed 4pm", "Wed 5pm", "Wed 6pm", "Wed 7pm",
                         "Thu 8am", "Thu 9am", "Thu 10am", "Thu 11am", "Thu 12pm", "Thu 1pm", "Thu 2pm", "Thu 3pm",
                         "Thu 4pm", "Thu 5pm", "Thu 6pm", "Thu 7pm",
                         "Fri 8am", "Fri 9am", "Fri 10am", "Fri 11am", "Fri 12pm", "Fri 1pm", "Fri 2pm", "Fri 3pm",
                         "Fri 4pm", "Fri 5pm", "Fri 6pm", "Fri 7pm"]},
    {"name": "12",
     "available_slots": ["Mon 8am", "Mon 9am", "Mon 10am", "Mon 11am", "Mon 12pm", "Mon 1pm", "Mon 2pm", "Mon 3pm",
                         "Mon 4pm", "Mon 5pm", "Mon 6pm", "Mon 7pm",
                         "Tue 8am", "Tue 9am", "Tue 10am", "Tue 11am", "Tue 12pm", "Tue 1pm", "Tue 2pm", "Tue 3pm",
                         "Tue 4pm", "Tue 5pm", "Tue 6pm", "Tue 7pm",
                         "Wed 8am", "Wed 9am", "Wed 10am", "Wed 11am", "Wed 12pm", "Wed 1pm", "Wed 2pm", "Wed 3pm",
                         "Wed 4pm", "Wed 5pm", "Wed 6pm", "Wed 7pm",
                         "Thu 8am", "Thu 9am", "Thu 10am", "Thu 11am", "Thu 12pm", "Thu 1pm", "Thu 2pm", "Thu 3pm",
                         "Thu 4pm", "Thu 5pm", "Thu 6pm", "Thu 7pm",
                         "Fri 8am", "Fri 9am", "Fri 10am", "Fri 11am", "Fri 12pm", "Fri 1pm", "Fri 2pm", "Fri 3pm",
                         "Fri 4pm", "Fri 5pm", "Fri 6pm", "Fri 7pm"]}
]

# Define professors and their availability
professors_data = [
    {"name": "Prof. Igor", "subjects": ["VNP", "OS", "OOP"], "unavailable_slots": ["Mon", "Tue 9am"]},
    {"name": "Prof. Riste", "subjects": ["OS", "E-Vlada", "OOP"],
     "unavailable_slots": ["Tue 7pm", "Wed 10am", "Thu 11am", "Fri 12pm"]},
    {"name": "Prof. Andrea", "subjects": ["VNP", "OS", "DS"], "unavailable_slots": ["Mon 10am", "Tue 2pm", "Wed 11am"]},
    {"name": "Prof. Mile", "subjects": ["VNP", "OOP", "SP"], "unavailable_slots": ["Thu 1pm", "Fri 3pm"]},
    {"name": "Prof. Ilinka", "subjects": ["VNP", "DS", "Pretpriemnistvo"], "unavailable_slots": ["Fri 9am", "Fri 4pm"]},
]