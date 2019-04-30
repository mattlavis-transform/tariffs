import psycopg2
from docx import Document
from docx.shared import Inches
from docx.shared import Cm
from docx.oxml.shared import OxmlElement, qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.enum.text import WD_TAB_LEADER
import os
import csv
import sys
import codecs
import re
import functions
import xlsxwriter

from measure import measure
from component import component
from footnote import footnote
from condition import condition

def writeOrderNumberRows(sOrderNumber):
	global conn 
	global worksheet
	global lRow
	###############################################################
	# Get the definitions
	sSQL = """SELECT DISTINCT qon.quota_order_number_sid, qd.validity_start_date as defintion_start_date, qd.validity_end_date as defintion_end_date,
	qd.initial_volume, qd.measurement_unit_code, qd.maximum_precision, qd.critical_state, qd.critical_threshold, qd.monetary_unit_code, qd.measurement_unit_qualifier_code, qd.description
	FROM measures m, quota_definitions qd, quota_order_numbers qon
	WHERE m.ordernumber = qd.quota_order_number_id
	AND m.ordernumber = qon.quota_order_number_id
	AND m.validity_start_date > (CURRENT_DATE - 365)
	AND qd.validity_start_date > (CURRENT_DATE - 365)
	AND m.ordernumber = '""" + sOrderNumber + """'
	ORDER BY 1, 2;"""
	
	cur = conn.cursor()
	cur.execute(sSQL)
	rows_definitions = cur.fetchall()
	
	# Get the definitions
	for m in rows_definitions:
		quota_order_number_sid          = m[0]
		definition_start_date           = m[1]
		definition_end_date             = m[2]
		initial_volume                  = m[3]
		measurement_unit_code           = m[4]
		maximum_precision               = m[5]
		critical_state                  = m[6]
		critical_threshold              = m[7]
		monetary_unit_code              = m[8]
		measurement_unit_qualifier_code = m[9]
		description                     = m[10]

		print (sOrderNumber, lRow)
		
		worksheet.write(lRow, 0,  sOrderNumber, cfWrap)
		worksheet.write(lRow, 1,  quota_order_number_sid, cfWrap)
		worksheet.write(lRow, 2,  definition_start_date, cfWrap)
		worksheet.write(lRow, 3,  definition_end_date, cfWrap)
		worksheet.write(lRow, 4,  initial_volume, cfWrap)
		worksheet.write(lRow, 5,  measurement_unit_code, cfWrap)
		worksheet.write(lRow, 6,  maximum_precision, cfWrap)
		worksheet.write(lRow, 7,  critical_state, cfWrap)
		worksheet.write(lRow, 8,  critical_threshold, cfWrap)
		worksheet.write(lRow, 9,  monetary_unit_code, cfWrap)
		worksheet.write(lRow, 10, measurement_unit_qualifier_code, cfWrap)
		worksheet.write(lRow, 11, description, cfWrap)
		lRow = lRow + 1

	
conn = psycopg2.connect("dbname=trade_tariff_1809 user=postgres password=" + self.p)

sSQL = """SELECT DISTINCT m.ordernumber FROM measures m WHERE m.validity_start_date > (CURRENT_DATE - 365) ORDER BY 1;"""
cur = conn.cursor()
cur.execute(sSQL)
rows_ordernumbers = cur.fetchall()
i = 1
lRow = 1

# Write the Excel file
sFilename = "C:\\projects\\create_quota_sheet\\excel\\quotas.xlsx"

workbook = xlsxwriter.Workbook(sFilename)
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': 'black'})
bold.set_font_size(9)

cfWrap = workbook.add_format()
cfWrap.set_text_wrap()
cfWrap.set_align('left')
cfWrap.set_align('top')
cfWrap.set_font_size(9)
cfWrap.set_font_name('Calibri')

worksheet.write('A1', 'Order number', bold)
worksheet.write('B1', 'Order number SID', bold)
worksheet.write('C1', 'Definition start date', bold)
worksheet.write('D1', 'Definition end date', bold)
worksheet.write('E1', 'Initial volume', bold)
worksheet.write('F1', 'Measurement unit code', bold)
worksheet.write('G1', 'Maximum precision', bold)
worksheet.write('H1', 'Critical state', bold)
worksheet.write('I1', 'Critical threshold', bold)
worksheet.write('J1', 'Monetary unit code', bold)
worksheet.write('K1', 'Measurement unit qualifier code', bold)
worksheet.write('L1', 'Description', bold)

worksheet.set_column("A:A", 12)
worksheet.set_column("B:B", 25)
worksheet.set_column("C:D", 15)
worksheet.set_column("E:E", 20)
worksheet.set_column("F:F", 20)
worksheet.set_column("G:G", 12)
worksheet.set_column("H:H", 32)
worksheet.set_column("I:I", 80)
worksheet.set_column("J:J", 60)
worksheet.set_column("K:K", 60)
worksheet.set_column("L:L", 60)

for m in rows_ordernumbers:
	sOrderNumber = m[0]
	writeOrderNumberRows(sOrderNumber)
	i = i + 1
	if i > 10:
		sys.exit()

conn.close()
worksheet.freeze_panes(1, 0)
workbook.close()