# one course only
# {
#   modifers=[] ex.cannot be dual counted
#   relationship = [] ex. and/or/null between the list of courses
#   courses = [] ex. a list of courses
# }
import json

"""
{
    "modifiers":[],
    "course": "HUM 101",
    "name": "Introduction to Humanities",
    "units": 3
}
"""
class course:
    def __init__(self, modifers=[], course_n="", name="", units=0):
        
        self.modifers = modifers
        self.course_number = course_n
        self.name = name
        self.units = units
        """
        self.course = [{
            "modifers": modifers,
            "course": course_n,
            "name": name,
            "units": units,
        }]
        """

        

"""
{
    "relationship": "or",
    "courses": [
        {
            "modifiers":[],
            "course": "HUM 101",
            "name": "Introduction to Humanities",
            "units": 3
        },
        {
            "modifers":["Cannot be dual counted"],
            "course" : "BUS 101",
            "name" : "Introduction to Business",
            "units":4
        }
    ],
}
"""
class courses:
    def __init__(self, relationship="and", courses=[],):
        self.relationship = relationship
        self.courses = courses
        """
        self.courses_list = {
            "relationship": self.relationship,
            "courses": self.courses,
        }
        """

    def add_course(self, course):
        self.courses_list["courses"].append(course)

"""
{
    "univ":{
        "relationship": "and",
        "courses_row": [
            {
                "relationship": "or",
                "courses": [
                {
                    "modifiers":[],
                    "course": "HUM 101",
                    "name": "Introduction to Humanities",
                    "units": 3
                },
                {
                    "modifers":["Cannot be dual counted"],
                    "course" : "BUS 101",
                    "name" : "Introduction to Business",
                    "units":4
                }
                ],
            },
            {
                relationship":"and",
                "courses":[
                    {
                        "modifiers":[],
                        "course": "HUM 101",
                        "name": "Introduction to Humanities",
                        "units": 3
                    }
                ],
            }],
    },
    "cc":{
        "relationship":"and",
        "courses_row": [
            {
                "relationship": "or",
                "courses": [
                {
                    "modifiers":[],
                    "course": "HUM 101",
                    "name": "Introduction to Humanities",
                    "units": 3
                },
                {
                    "modifers":["Cannot be dual counted"],
                    "course" : "BUS 101",
                    "name" : "Introduction to Business",
                    "units":4
                }
                ],
            },
        ],
    }
}
"""
class pair:
    def __init__(self, u_course=[], c_course=[], u_r="and", c_r="and",):
        self.univ_course = u_course
        self.univ_r = u_r
        self.cc_course = c_course
        self.cc_r = c_r
        """
        self.pair = {
            "univ": {
                "relationship": self.u_r,
                "courses_row": self.u_course
            },
            "cc": {
                "relationship": self.c_r,
                "name":self.c_course
            }
        }
        """

# relationship between a list of pairs
class section:
    def __init__(self, header="", info="null", pairs=[], next_relationship="and",):
        self.header = header
        self.info = info
        self.pairs = pairs
        self.next_relationship = next_relationship
        """
        self.section = {
            "section_name": self.header,
            "info": self.info,
            "next relationship": self.next_relationship,
            "articulations": self.pairs
        }
        """

"""
# relationship between sections if sections are big
class sections(section):
    def __init__(self, section_list=[]):
        self.section_list = section_list
        
        self.sections = {
            "sections": self.section_list,
        }
        
"""
class page:
    def __init__(self, title={}, all_sections=[]):
        self.title = title
        self.all_sections = all_sections
        """
        self.overall = {
            "header": self.title,
            "page": self.all_sections
        }
        """





    



