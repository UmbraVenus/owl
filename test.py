from pairs import *
import json
"""
course_1 = course()
course_1.course = {
    "modifiers":[],
    "course": "HUM 101",
    "name": "Introduction to Humanities",
    "units": 3,
}

"""
course_2 = course()
course_2.modifers = ["Cannot be dual counted"]
course_2.course_number = "BUS 101"
course_2.name = "Intro to business"
course_2.units = 3

data = json.dumps(course_2.__dict__)

with open("data_file.json", "w", encoding='utf-8') as write_file:
    write_file.write(data)

print(data)