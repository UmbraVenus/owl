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

def clean(string):
    if type(string) == np.float64:
        return string
    while string.startswith(" "):
        astring = string[1:]
        string = astring
    while string.endswith(" "):
        astring = string[:-1]
        string = astring
    return string.replace(u'\u200b', '').replace("\n", "")
    

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



def is_course(string):
    course_regex = re.compile(r'(← )*([A-Z])+ (\d)+(H)* - [a-zA-Z]+( (\d.\d\d))*')
    if course_regex.search(string) or string == "← No Course Articulated" or string == "Course cannot be dual counted" or "No Course Articulated" in string or (r'(← )*([A-Z])+ (\d)+(H)* - [a-zA-Z]+( (\d.\d\d))*') in string:
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
            for x in Table().read_table(fname).column(8):
                rawlist2.append(x)
    
    for fname in glob.glob(path):
        if re.search('^1-page-', fname) != None:
            try:
                os.remove(fname)
            except OSError as e:
                print("Error: %s : %s" % (fname, e.strerror))
    #print(len(rawlist))
    #print(len(rawlist2))
    rawlist = [clean(x) for x in rawlist]
    rawlist2 = [clean(x) for x in rawlist2]
    
    df = pd.DataFrame(
        {
            "univ": rawlist,
            "cc":rawlist2,
        },
    )
    #df.to_csv("3.csv")
    df = df.fillna("nan")
    return df

def contains_courses(df):
    for index, row in df.iterrows():
        if is_course(row["univ"]) or is_course(row["cc"]):
            return True
    return False

# slicing the df into different categories
#def
def get_sections(df1):
    header_index = []
    for index, row in df1[:-1].iterrows():
        """
        if row["cc"].startswith("TRACK") or "Only lower" in row["cc"]  or (((not (row["cc"].startswith(" **"))) and row["cc"].isupper()) and (df1.iloc[index + 1]["cc"].startswith("Select 1") or df1.iloc[index + 1]["cc"].startswith(" **REFER TO") or is_course(df1.iloc[index + 1]["univ"]) or df1.iloc[index + 1]["cc"].startswith(" Only lower"))):
            print("=======")
            if not row["cc"].startswith(" **"):
                header_index.append(index)
        elif "Only lower" in row["cc"]:
            header_index.append(index)
        """
        if row["cc"].isupper():
            header_index.append(index)
    newlist = []
    if len(header_index) > 1:
        newlist = [df1[header_index[i] : header_index[i + 1]] for i in range(len(header_index) - 1)] + [df1[header_index[-1] :]]
    newerlist = []
    
    for i, x in enumerate(newlist):
        if contains_courses(x):
            newerlist.append(x)
        else:
            continue
    print(header_index)
    print(newerlist)
    return newerlist

def create_course(info):
    new_course = course()
    new_course.course = get_course_info(info)
    return new_course

# inputs a section df, outputs a list of courses
def get_courses_list(df2):
    #big or
    #print(df2)
    pair_list = []
    length = len(df2["univ"])+1
    s2 = pd.Series([["nanhuh", "nankjhg",]], index=[length])
    df2 = df2.append(s2, ignore_index=True)
    s3 = pd.Series([["nanhhgg", "nangjj",]], index=[length])
    df2 = df2.append(s3, ignore_index=True)
    df2 = df2.fillna("nan")
    for index, row in df2.iterrows():
        # no relationship
        if is_course(row["univ"]) and not has_r(df2.iloc[index + 1]["univ"]) and is_course(row["cc"]) and not has_r(df2.iloc[index + 1]["cc"]):
            new_pair = pair()
            cc_courses = []
            univ_courses = []
            univ_r = "null"
            cc_r = "null"
            new_cc_course = create_course(row["cc"])
            new_univ_course = create_course(row["univ"])
            cc_courses.append(new_cc_course.__dict__)
            univ_courses.append(new_univ_course.__dict__)
            new_pair.univ = univ_courses
            new_pair.cc = cc_courses
            pair_list.append(new_pair.__dict__)
        # univ relationship and big or
        elif is_course(row["univ"]) and not has_r(df2.iloc[index + 1]["univ"]) and is_course(row["cc"]) and has_r(df2.iloc[index + 1]["cc"]):
            new_pair = pair()
            cc_courses = []
            univ_courses = []
            univ_r = "null"
            cc_r = "null"
            new_cc_course = create_course(row["cc"])
            new_univ_course = create_course(row["univ"])
            cc_courses.append(new_cc_course.__dict__)
            univ_courses.append(new_univ_course.__dict__)
            relationship = "null"
            for i, r in df2[index+1:].iterrows():
                #print(r)
                if has_r(r["cc"]):
                    relationship = r["cc"].strip("-").strip(" ")
                elif is_course(r["cc"]) and not is_course(r["univ"]):
                    #relationship = df2.iloc[i-1]["cc"].strip("-").strip(" ")
                    newer_cc_course = create_course(r["cc"])
                    cc_courses.append(newer_cc_course.__dict__)
                    new_pair.cc_relationship = relationship
                    relationship = "null"
                else:
                    break
            new_pair.univ = univ_courses
            new_pair.cc = cc_courses
            pair_list.append(new_pair.__dict__)
        elif is_course(row["univ"]) and (has_r(df2.iloc[index + 1]["univ"]) or has_r(df2.iloc[index+1]["cc"])):
            print("=======")
            new_pair = pair()
            cc_courses = []
            univ_courses = []
            univ_r = "null"
            cc_r = "null"
            new_cc_course = create_course(row["cc"])
            new_univ_course = create_course(row["univ"])
            cc_courses.append(new_cc_course.__dict__)
            univ_courses.append(new_univ_course.__dict__)
            relationship = min(df2.iloc[index+1]["cc"].strip("-").strip(" "), df2.iloc[index+1]["univ"].strip("-").strip(" "))
            for i, r in df2[index + 1 :].iterrows():
                #print(r)
                if has_r(r["univ"]):
                    relationship = r["cc"].strip("-").strip(" ")
                elif is_course(r["univ"]) and r["cc"]=="nan":
                    new_pair.univ_relationship = relationship
                    newer_univ_course = create_course(r["univ"])
                    univ_courses.append(newer_univ_course.__dict__)
                    break
                else:
                    #print("=======")
                    if is_course(r["cc"]) or is_course(r["univ"]):
                        new_pair.next_relationship = relationship
                        new_pair.univ = univ_courses
                        new_pair.cc = cc_courses
                        pair_list.append(new_pair.__dict__)
                        relationship = "null"
                        newer_pair = pair()
                        cc_courses = []
                        univ_courses = []
                        newer_cc_course = create_course(r["cc"])
                        newer_univ_course = create_course(r["univ"])
                        cc_courses.append(newer_cc_course.__dict__)
                        univ_courses.append(newer_univ_course.__dict__)
                        newer_pair.univ = univ_courses
                        newer_pair.cc = cc_courses
                        pair_list.append(newer_pair.__dict__)
                        break
            new_pair.univ = univ_courses
            new_pair.cc = cc_courses
            pair_list.append(new_pair.__dict__)
        # cc relationship
    return pair_list

def get_object(df, filename):
    uni = clean(df.iloc[1]["univ"].split(":")[1])
    cc = clean(df.iloc[1]["cc"].split(":")[1])
    route = df.iloc[3]["cc"]
    header = {
        "source": filename,
        "university": uni,
        "college": cc,
        "route": route
    }
    page_list = []
    sections_list = get_sections(df)
    for i, x in enumerate(sections_list):
        x.reset_index()
        new_section = section()
        new_section.section_name = x.iloc[0]["cc"]
        if not is_course(x.iloc[1]["cc"]):
            new_section.info = x.iloc[1]["cc"]
        else:
            new_section.info = "null"
        
        if has_r(x.iloc[-1]["cc"]):
            new_section.next_relationship = x.iloc[-1]["cc"].strip("-").strip(" ")
        
        new_section.articulations = get_courses_list(x)
        page_list.append(new_section.__dict__)
    final = page()
    final.header = header
    final.sections = page_list
    return final.__dict__

def get_json(final_object, output_file):
    with open(output_file, 'w') as fp:
        json.dump(final_object, fp)


#df = read_table("owl/Student_TestSet/19.pdf")
#final_object = get_object(df, "owl/Student_TestSet/19.pdf")
#get_json(final_object, "data_file.json")