# one course only
# {
#   modifers=[] ex.cannot be dual counted
#   relationship = [] ex. and/or/null between the list of courses
#   courses = [] ex. a list of courses
# }
import json

"""
"or": [ "PHIL 101", "PHIL 101H" ]
"""
class or_r:
    def __init__(self, or_list=[]):
        self.or_r = or_list
    
    def addor(self, objects):
        self.or_r.append(objects)
        
class and_r:
    def __init__(self, and_list=[]):
        self.and_r = and_list
    def addand(self, objects):
        self.and_r.append(objects)


"""
{
	"modifiers": [],
	"course": "HUM 105"
},
"""
class course:
    def __init__(self, modifers=[], course="", name=""):
        
        self.modifers = modifers
        self.course = course
        #self.name = name
        #self.name = name
        #self.units = units
        """
        self.course = [{
            "modifers": modifers,
            "course": course_n,
            "name": name,
            "units": units,
        }]
        """

        


class courses:
    def __init__(self, relationship="null", courses=[],):
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
					"univ": {
						"modifiers": [],
						"course": "HUM 105"
					},
					"cc": {
						"modifiers": [],
						"name": "No Course Articulated"
					}
				},
"""
class pair:
    def __init__(self, u_course=[], c_course=[],):
        self.univ = u_course
        #self.univ_r = u_r
        self.cc = c_course
        #self.cc_r = c_r
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
    def __init__(self, section_name="", info="null", articulations=[],):
        self.section_name = section_name
        self.info = info
        self.articulations = articulations
        #self.next_relationship = next_relationship
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
    def __init__(self, header={}, sections=[]):
        self.header = header
        self.sections = sections
        """
        self.overall = {
            "header": self.title,
            "page": self.all_sections
        }
        """





    



