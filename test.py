import tabula
tables = tabula.read_pdf("owl/Student_TestSet/18.pdf", pages="all", stream=True,)
print(tables)