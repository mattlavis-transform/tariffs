# Imported modules
import csv
import os
import codecs
from csv import QUOTE_ALL
import xlsxwriter

# custom modules
import common.objects as o

app = o.app
sFilename = os.path.join(app.SOURCE_DIR, "footnotes.xlsx")

workbook = xlsxwriter.Workbook(sFilename)
bold = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': 'black'})
bold.set_font_size(9)

cfWrap = workbook.add_format()
cfWrap.set_text_wrap()
cfWrap.set_align('left')
cfWrap.set_align('top')
cfWrap.set_font_size(9)
cfWrap.set_font_name('Calibri')

# Create the updated footnotes sheet
worksheet = workbook.add_worksheet("Updated")
worksheet.write('A1', 'FOOTNOTE_TYPE_ID', bold)
worksheet.write('B1', 'FOOTNOTE_ID', bold)
worksheet.write('C1', 'DESCRIPTION_OLD', bold)
worksheet.write('D1', 'DESCRIPTION_NEW', bold)

worksheet.set_column("A:A", 15)
worksheet.set_column("B:B", 15)
worksheet.set_column("C:C", 75)
worksheet.set_column("D:D", 75)

app.getFoonotes()
app.resolveFootnotes()
row = 1
for f in app.footnotes_list:
    worksheet.write(row, 0,  f.footnote_type_id, cfWrap)
    worksheet.write(row, 1,  f.footnote_id, cfWrap)
    worksheet.write(row, 2,  f.description, cfWrap)
    worksheet.write(row, 3,  f.description, cfWrap)
    row += 1


# Create the new footnotes sheet
worksheet2 = workbook.add_worksheet("New")
worksheet2.write('A1', 'FOOTNOTE_TYPE_ID', bold)
worksheet2.write('B1', 'FOOTNOTE_ID', bold)
worksheet2.write('C1', 'DESCRIPTION', bold)

worksheet2.set_column("A:A", 15)
worksheet2.set_column("B:B", 15)
worksheet2.set_column("C:C", 75)

worksheet.freeze_panes(1, 0)
workbook.close()