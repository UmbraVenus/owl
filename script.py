import camelot
import pandas as pd
from datascience import *
import glob
import re
import numpy as np

#tables = camelot.read_pdf("owl/Student_TestSet/3.pdf", flavor="lattice", process_background=True, line_scale=130, backend="poppler",pages="all", layout_kwargs={'detect_vertical': False})

tables = camelot.read_pdf("owl/Student_TestSet/3.pdf", flavor="stream", table_areas=['28,810,534,33'],pages="all",)

header = []
hr = []
left = []
rela = []
right = []

result = Table().with_columns(
    "header", header,
    "header relationship", hr,
    "left", left,
    "relationship",rela,
    "right",right,
)

raw = Table()

#print(tables[0].df)
tables.export('1.csv')
path = "*.csv"
rawlist = []
for fname in glob.glob(path):
    if re.search('^1-page-', fname) != None:
        rawlist += [Table().read_table(fname).column(0)]

rawlist = np.array(rawlist, dtype=object)
raw = raw.with_column("raw",rawlist)
        
"""
for x in tables:
    for i in range(len(x)):
"""
def transform(rawlist):
    dictionary = {}
    for x in rawlist:
        for y in x:
            