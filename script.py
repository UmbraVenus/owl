import camelot
import pandas as pd
from datascience import *
import glob
import re
import numpy as np
from pairs import *
import json
from fuzzywuzzy import fuzz

#tables = camelot.read_pdf("owl/Student_TestSet/3.pdf", flavor="lattice", process_background=True, line_scale=130, backend="poppler",pages="all", layout_kwargs={'detect_vertical': False})

# inputs a string, gets a list of all strings in pdf
def read_table(filename):
    tables = camelot.read_pdf(filename, flavor="stream", table_areas=['28,810,534,33'], pages="all",)
    
    #raw = Table()

    #print(tables[0].df)
    tables.export('1.csv')
    path = "*.csv"
    rawlist = []
    for fname in glob.glob(path):
        if re.search('^1-page-', fname) != None:
            for x in Table().read_table(fname).column(0):
                rawlist.append(x)

    #print(rawlist)
    return rawlist

# find out if section or course has relationship to it
def has_r(prev):
    if prev == "--- And ---" or prev == "--- Or ---":
        return True
    return False

# extract course information, course no, name, and units
def get_course_info(string):
    new_str = string.strip("←").split("-")
    course_n = new_str[0]
    newer_str = ""
    if len(new_str)>1:
        newer_str = new_str[1].split("(")
        name = newer_str[0]
    else:
        name = "null"

    if len(newer_str)>1:
        units = newer_str[1][0:4]
    else:
        units = "null"
    return [course_n.replace(u'\u200b',''), name.replace(u'\u200b',''), units]

def get_object(rawlist, filename):
    if rawlist[1] != "nan":
        uni = rawlist[1].split(":",)
    
        university, college = uni[1][0:-5], uni[2]
        route = rawlist[3]
        header = {
        "source": filename,
        "university": university,
        "college": college,
        "route": route
        }
    else:
        header = {
        "source": "nan",
        "university": "nan",
        "college": "nan",
        "route": "nan"
        }
    header_index = []
    new_rawlist = rawlist[4:-1]
    for i, x in enumerate(new_rawlist):
        # get lists of sections, and its relationship
        if x.upper() == x and (new_rawlist[i+1].startswith("Select 1") or new_rawlist[i+1].startswith("**REFER TO") or new_rawlist[i+1].startswith("←")) and (not re.sub('[^A-Za-z0-9]+', '', x).isnumeric()) and (x not in [new_rawlist[x] for x in header_index]):
            header_index.append(i)
    newlist = [new_rawlist[header_index[i] : header_index[i + 1]] for i in range(len(header_index) - 1)] + [new_rawlist[header_index[-1]:]]
    
    page_list = []
    sections_list=[]
    for i, x in enumerate(newlist):
        new_section = section()
        section_name = x[0]
        if not x[1].startswith("←"):
            info = x[1]
        else:
            info = "null"
        if has_r(x[-1]):
            next_relationship = x[-1].strip("-").strip(" ")
        else:
            next_relationship = "null"
        new_section.section_name = section_name
        new_section.info = info
        new_section.next_relationship = next_relationship
        new_section.articulations = []
        page_list.append(new_section)

        s_index = []
        for index, y in enumerate(x):
            if y.startswith("←"):
                s_index.append(index)
        one_pair = [x[s_index[i] : s_index[i + 1]] for i in range(len(s_index) - 1)] + [x[s_index[-1] :]]
        sections_list.append(one_pair)
   
    for index, x in enumerate(sections_list):
        page_list[index].articulations = []
        for idx, z in enumerate(x):
            new_pair = pair()
            cc_courses = []
            univ_courses = []
            univ_r = "null"
            cc_r = "null"
            for i, y in enumerate(z):
                if y.startswith("←") and y != "← No Course Articulated":
                    new_cc_course = course()
                    course_info = get_course_info(y)
                    new_cc_course.course, new_cc_course.name, new_cc_course.units = course_info[0], course_info[1], course_info[2]
                    if len(z) > 3:
                        if z[i + 3] == "Course cannot be dual counted":
                            new_cc_course.modifers = ["Course cannot be dual counted"]
                    cc_courses.append(new_cc_course.__dict__)
        
                    new_u_course = course()
                    univ_course_info = get_course_info(z[i+1])
                    new_u_course.course, new_u_course.name, new_u_course.units = univ_course_info[0], univ_course_info[1], univ_course_info[2]
                    univ_courses.append(new_u_course.__dict__)
                    
                elif y.startswith("← No Course Articulated"):
                    new_cc_course = course()
                    course_info = get_course_info(y)
                    new_cc_course.course, new_cc_course.name, new_cc_course.units = course_info[0], course_info[1], course_info[2]
                    if len(z) > 3:
                        if z[i + 3] == "Course cannot be dual counted":
                            new_cc_course.modifers = ["Course cannot be dual counted"]
                    cc_courses.append(new_cc_course.__dict__)

                    new_u_course = course()
                    univ_course_info = get_course_info(z[i+1])
                    new_u_course.course, new_u_course.name, new_u_course.units = univ_course_info[0], univ_course_info[1], univ_course_info[2]
                    univ_courses.append(new_u_course.__dict__)
                
                if has_r(y):
                    if i < len(z)-1:
                        score_c = fuzz.ratio(z[i + 1], z[i - 2])
                        score_u = fuzz.ratio(z[i + 1], z[i - 1])
                        if score_c > score_u:
                            new_pair.cc_r = y.strip("-")
                            newer_cc_course = course()
                            newer_cc_info = get_course_info(z[i + 1])
                            newer_cc_course.course, newer_cc_course.name, newer_cc_course.units = newer_cc_info[0], newer_cc_info[1], newer_cc_info[2]
                            cc_courses.append(newer_cc_course.__dict__)
                        elif score_u > score_c:
                            new_pair.univ_r = y.strip("-")
                            newer_u_course = course()
                            newer_u_info = get_course_info(z[i + 1])
                            newer_u_course.course, newer_u_course.name, newer_u_course.units = newer_u_info[0], newer_u_info[1], newer_u_info[2]
                            univ_courses.append(newer_u_course.__dict__)
                new_pair.univ_course = univ_courses
                new_pair.cc_course = cc_courses
            page_list[index].articulations.append(new_pair.__dict__)
    new_page_list = [x.__dict__ for x in page_list]
    final = page()
    final.header = header
    final.sections = new_page_list
    return final.__dict__
    #print(sections_list)

def get_json(final_object, output_file):
    with open(output_file, 'w') as fp:
        json.dump(final_object, fp)


rawlist = read_table("owl/Student_TestSet/3.pdf")
final_object = get_object(rawlist, "owl/Student_TestSet/3.pdf")
get_json(final_object, "data_file.json")