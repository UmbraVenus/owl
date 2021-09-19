import camelot
import pandas as pd
from datascience import *
import glob
import re
import numpy as np
from pairs import *
import json
from fuzzywuzzy import fuzz
import os
import numpy as np
import tabula

def clean(string):
    while string.startswith(" "):
        astring = string[1:]
        string = astring
    while string.endswith(" "):
        astring = string[:-1]
        string = astring
    return string.replace(u'\u200b', '').replace("\n","")

def is_course(string):
    course_regex = re.compile(r'(← )*([A-Z])+ (\d)+(H)* - [a-zA-Z]+( (\d.\d\d))*')
    if course_regex.search(string) or string == "← No Course Articulated" or string == "Course cannot be dual counted":
        #print(True)
        return True
    else:
        #print(False)
        return False

# inputs a string(filename), gets a list of all strings in pdf
def read_table(filename):
    tables = camelot.read_pdf(filename, flavor="stream", table_areas=['0,842,591,0'], pages="all", row_tol=8, col_tol=250, columns=["262, 842, 284,0,569,842,592,0"])
    
    
    #raw = Table()

    #print(tables[0].df)
    tables.export('1.csv')

    path = "*.csv"
    rawlist = []
    rawlist2 = []
    
    for fname in glob.glob(path):
        if re.search('^1-page-', fname) != None:
            for x in Table().read_table(fname).column(0):
                rawlist.append(x)
    
    for fname in glob.glob(path):
        if re.search('^1-page-', fname) != None:
            try:
                os.remove(fname)
            except OSError as e:
                print("Error: %s : %s" % (fname, e.strerror))
    rawlist = [clean(x) for x in rawlist if not type(x)==np.float64]
    for x in rawlist:
        print(x)
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
    """
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
    """
    course_n = clean(course_n)
    return course_n


def get_object(rawlist, filename):
    if rawlist[0] != "nan":
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
    new_rawlist = rawlist[4:]
    #print(new_rawlist)
    for i, x in enumerate(new_rawlist):
        # get lists of sections, and its relationship
        if i < len(new_rawlist)-1:
            if x.upper() == x and (new_rawlist[i+1].startswith("Select 1") or new_rawlist[i+1].startswith("**REFER TO") or new_rawlist[i+1].startswith("←")) and (not re.sub('[^A-Za-z0-9]+', '', x).isnumeric()) and (x not in [new_rawlist[x] for x in header_index]):
                header_index.append(i)
    newlist = []
    if len(header_index)>1:
        newlist = [new_rawlist[header_index[i] : header_index[i + 1]] for i in range(len(header_index) - 1)] + [new_rawlist[header_index[-1] :]]
    
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
        

        new_section.section_name = section_name
        new_section.info = info
        new_section.next_relationship = next_relationship
        new_section.articulations = []
        """
        if has_r(x[-1]):
            r_list = []
            next_relationship = x[-1].strip("-").strip(" ")
            if next_relationship == "Or":
                giant_or = or_r()
                giant_or.or_r.addor(new_section)
                r_list.append(giant_or.__dict__)
            else:
                giant_and = and_r()
                giant_and.and_r.addand(new_section)
                r_list.append(giant_and.__dict__)
            page_list.append(r_list)
        else:
        """
        page_list.append(new_section)

        s_index = []
        for index, y in enumerate(x):
            if y.startswith("←"):
                s_index.append(index)
        one_pair = [x[s_index[i] : s_index[i + 1]] for i in range(len(s_index) - 1)]
        sections_list.append(one_pair)

    new_section_list = []
    for i, x in enumerate(sections_list):
        new_s_list = []
        for y in x:
            newy = y.copy()
            for z in y:
                #print(z)
                if is_course(z) or has_r(z):
                    continue
                else:
                    while z in newy:
                        newy.remove(z)
            new_s_list.append(newy)
        new_section_list.append(new_s_list)
    
    for i in range(len(new_section_list)):
        page_list[i].articulations = []
        #print(page_list[i])
        #print('----')
        #print(new_section_list[i])
    
    for index, x in enumerate(new_section_list):
        page_list[index].articulations = []
        for idx, z in enumerate(x):
            new_pair = pair()
            cc_courses = []
            univ_courses = []
            univ_r = "null"
            cc_r = "null"
            #print("======")
            #print(z)
            if has_r(z[-1]):
                for i, y in enumerate(z):
                    if y.startswith("←") and y != "← No Course Articulated":
                        new_cc_course = course()
                        course_info = get_course_info(y)
                        new_cc_course.course = course_info
                        if len(z) > 2:
                            if z[i + 2] == "Course cannot be dual counted":
                                new_cc_course.modifers = ["Course cannot be dual counted"]
                        cc_courses.append(new_cc_course.__dict__)
                        if len(z) > 1:
                            new_u_course = course()
                            univ_course_info = get_course_info(z[i+1])
                            new_u_course.course = univ_course_info
                            univ_courses.append(new_u_course.__dict__)
                        
                    elif y.startswith("← No Course Articulated"):
                        new_cc_course = course()
                        course_info = get_course_info(y)
                        new_cc_course.course = course_info
                        if len(z) > 3:
                            if z[i + 3] == "Course cannot be dual counted":
                                new_cc_course.modifers = ["Course cannot be dual counted"]
                        cc_courses.append(new_cc_course.__dict__)

                        if len(z) > 1:
                            new_u_course = course()
                            univ_course_info = get_course_info(z[i+1])
                            new_u_course.course = univ_course_info
                            univ_courses.append(new_u_course.__dict__)
                    
                    if has_r(y) and (not has_r(z[i-1])):
                        if i < len(z)-1:
                            score_c = fuzz.ratio(z[i + 1], z[i - 2])
                            score_u = fuzz.ratio(z[i + 1], z[i - 1])
                            if score_c > score_u:
                                new_pair.cc_r = y.strip("-")
                                newer_cc_course = course()
                                newer_cc_info = get_course_info(z[i + 1])
                                newer_cc_course.course = newer_cc_info
                                cc_courses.append(newer_cc_course.__dict__)
                            elif score_u > score_c:
                                new_pair.univ_r = y.strip("-")
                                newer_u_course = course()
                                newer_u_info = get_course_info(z[i + 1])
                                newer_u_course.course = newer_u_info
                                univ_courses.append(newer_u_course.__dict__)

                    new_pair.univ = univ_courses
                    new_pair.cc = cc_courses
                    new_pair.next_relationship = z[-1].strip("-").strip(" ")
                page_list[index].articulations.append(new_pair.__dict__)
            else:
                for i, y in enumerate(z):
                    if y.startswith("←") and y != "← No Course Articulated":
                        new_cc_course = course()
                        course_info = get_course_info(y)
                        new_cc_course.course = course_info
                        if len(z) > 2:
                            if z[i + 2] == "Course cannot be dual counted":
                                new_cc_course.modifers = ["Course cannot be dual counted"]
                        cc_courses.append(new_cc_course.__dict__)
                        if len(z) > 1:
                            new_u_course = course()
                            univ_course_info = get_course_info(z[i+1])
                            new_u_course.course = univ_course_info
                            univ_courses.append(new_u_course.__dict__)
                        
                    elif y.startswith("← No Course Articulated"):
                        new_cc_course = course()
                        course_info = get_course_info(y)
                        new_cc_course.course = course_info
                        if len(z) > 3:
                            if z[i + 3] == "Course cannot be dual counted":
                                new_cc_course.modifers = ["Course cannot be dual counted"]
                        cc_courses.append(new_cc_course.__dict__)

                        if len(z) > 1:
                            new_u_course = course()
                            univ_course_info = get_course_info(z[i+1])
                            new_u_course.course = univ_course_info
                            univ_courses.append(new_u_course.__dict__)
                    
                    if has_r(y) and (not has_r(z[i-1])):
                        if i < len(z)-1:
                            score_c = fuzz.ratio(z[i + 1], z[i - 2])
                            score_u = fuzz.ratio(z[i + 1], z[i - 1])
                            if score_c > score_u:
                                new_pair.cc_r = y.strip("-")
                                newer_cc_course = course()
                                newer_cc_info = get_course_info(z[i + 1])
                                newer_cc_course.course = newer_cc_info
                                cc_courses.append(newer_cc_course.__dict__)
                            elif score_u > score_c:
                                new_pair.univ_r = y.strip("-")
                                newer_u_course = course()
                                newer_u_info = get_course_info(z[i + 1])
                                newer_u_course.course = newer_u_info
                                univ_courses.append(newer_u_course.__dict__)

                    new_pair.univ = univ_courses
                    new_pair.cc = cc_courses
                    new_pair.next_relationship = "null"
                page_list[index].articulations.append(new_pair.__dict__)
    new_page_list = [x.__dict__ for x in page_list]
    final = page()
    final.header = header
    final.sections = new_page_list
    return final.__dict__

def get_json(final_object, output_file):
    with open(output_file, 'w') as fp:
        json.dump(final_object, fp)

rawlist = read_table("owl/Student_TestSet/10.pdf")
final_object = get_object(rawlist, "owl/Student_TestSet/10.pdf")
get_json(final_object, "data_file.json")