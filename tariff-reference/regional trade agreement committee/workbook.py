import psycopg2
import sys
import os
from os import system, name 
import xlsxwriter
import functions as f
from application import application

class workbook(object):
	def __init__(self):
		self.current_row = 7

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
		self.bold = self.wb.add_format({'bold': True, 'font_name':'Verdana'})
		self.title = self.wb.add_format({'bold': True, 'font_size': 20, 'font_name':'Verdana'})
		self.wrap = self.wb.add_format({'text_wrap': True, 'align': 'left', 'valign': 'top', 'font_name':'Verdana'})
		self.nowrap = self.wb.add_format({'text_wrap': False, 'align': 'left', 'valign': 'top', 'font_name':'Verdana'})
		self.center = self.wb.add_format({'text_wrap': False, 'align': 'center', 'valign': 'top', 'font_name':'Verdana'})
		self.boldcenter = self.wb.add_format({'bold': True, 'text_wrap': False, 'align': 'center', 'valign': 'top', 'font_name':'Verdana'})
		self.indent_formats = []
		for i in range(0, 14):
			tmp = self.wb.add_format({'text_wrap': True, 'align': 'left', 'valign': 'top', 'indent': i * 2, 'font_name':'Verdana'})
			self.indent_formats.append(tmp)

		self.superscript	= self.wb.add_format({'font_script': 1})
		self.subscript		= self.wb.add_format({'font_script': 2})
		
	def close_workbook(self):
		self.wb.close()

	def write_headers(self):
		self.worksheet.write('A1', 'Tariff Schedule and Import Data', self.title)
		self.worksheet.write('A2', 'RTA:', self.bold)
		self.worksheet.write('A3', 'Party to the Agreement: Reporter:', self.bold)

		self.worksheet.write('A5', 'Tariff line', self.boldcenter)
		self.worksheet.write('B5', 'Description', self.boldcenter)
		self.worksheet.write('C5', 'MFN applied rate', self.boldcenter)
		self.worksheet.write('D5', self.app.country_profile_formatted, self.boldcenter)
		self.worksheet.write('E5', 'Applied', self.boldcenter)
		self.worksheet.write('F5', 'PLS', self.boldcenter)
		self.worksheet.write('G5', 'Indent', self.boldcenter)
		self.worksheet.write('H5', 'Leaf', self.boldcenter)

		self.worksheet.write('A6', '(1)', self.center)
		self.worksheet.write('B6', '(2)', self.center)
		self.worksheet.write('C6', '(3)', self.center)

	def write(self, column, content, fmt):
		cl = column + str(self.current_row)
		self.worksheet.write(cl, content, fmt)