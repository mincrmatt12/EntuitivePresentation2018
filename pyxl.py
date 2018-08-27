import openpyxl

wb = openpyxl.load_workbook('test.xlsx')
sheet = wb.active   # active sheet

print(sheet["F5"])
for i in sheet.rows:
    print(i[0]) # first column in each row.
