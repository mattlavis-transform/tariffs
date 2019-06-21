import psycopg2
import sys
import os
from os import system, name 
import xlsxwriter
import functions as f
from application import application

class workbook(object):
	def __init__(self):
		self.current_row = 1

	def create_workbook(self, app):
		#print ("creating workbook")
		filename = app.country_profile + ".xlsx"
		self.app = app
		self.wb = xlsxwriter.Workbook(filename)
		self.worksheet = self.wb.add_worksheet()

		# Column widths
		self.worksheet.set_column('A:A', 20)
		self.worksheet.set_column('B:B', 70)
		self.worksheet.set_column('C:C', 40, None, {'hidden': 0})
		self.worksheet.set_column('D:D', 40, None, {'hidden': 0})
		self.worksheet.set_column('E:E', 40)
		self.worksheet.set_column('F:F', 10, None, {'hidden': 1})
		self.worksheet.set_column('G:G', 10, None, {'hidden': 1})
		self.worksheet.set_column('H:H', 10, None, {'hidden': 1})
		self.worksheet.freeze_panes(1, 0)

		
		# Cell formats
		self.bold = self.wb.add_format({'bold': True})
		self.wrap = self.wb.add_format({'text_wrap': True, 'align': 'left', 'valign': 'top'})
		self.nowrap = self.wb.add_format({'text_wrap': False, 'align': 'left', 'valign': 'top'})
		self.center = self.wb.add_format({'text_wrap': False, 'align': 'center', 'valign': 'top'})
		self.boldcenter = self.wb.add_format({'bold': True, 'text_wrap': False, 'align': 'center', 'valign': 'top'})
		self.indent_formats = []
		for i in range(0, 14):
			tmp = self.wb.add_format({'text_wrap': True, 'align': 'left', 'valign': 'top', 'indent': i * 2})
			self.indent_formats.append(tmp)

		self.superscript	= self.wb.add_format({'font_script': 1})
		self.subscript		= self.wb.add_format({'font_script': 2})
		
	def close_workbook(self):
		self.wb.close()

	def write_headers(self):
		self.worksheet.write('A1', 'Commodity code', self.bold)
		self.worksheet.write('B1', 'Description', self.bold)
		self.worksheet.write('C1', 'MFN duty', self.bold)
		self.worksheet.write('D1', self.app.country_profile_formatted, self.bold)
		self.worksheet.write('E1', 'Applied', self.bold)

		self.worksheet.write('F1', 'PLS', self.boldcenter)
		self.worksheet.write('G1', 'Indent', self.boldcenter)
		self.worksheet.write('H1', 'Leaf', self.boldcenter)


	def write(self, column, content, fmt):
		cl = column + str(self.current_row)
		self.worksheet.write(cl, content, fmt)