import psycopg2
import sys
import os
from os import system, name 
import csv
import json
from datetime import datetime

import functions as f
from partial_temporary_stop import partial_temporary_stop
from document import document


class application(object):
	def __init__(self):
		self.clear()
		self.siv_list               = []
		self.meursing_list			= []
		self.vessels_list           = []
		self.civilair_list			= []
		self.airworthiness_list		= []
		self.aircraft_list			= []
		self.pharmaceuticals_list	= []
		self.ita_list 				= []
		self.generalrelief_list		= []
		self.authoriseduse_list		= []
		self.seasonal_list			= []
		self.special_list			= []
		self.section_chapter_list	= []
		self.lstFootnotes			= []
		self.lstFootnotesUnique		= []
		self.debug					= False
		self.suppress_duties		= False
		self.country_codes			= ""
		self.siv_data_list			= []
		self.seasonal_fta_duties	= []
		
		self.partial_temporary_stops	= []

		self.BASE_DIR			= os.path.dirname(os.path.abspath(__file__))
		self.SOURCE_DIR			= os.path.join(self.BASE_DIR, "source")
		self.CSV_DIR			= os.path.join(self.BASE_DIR, "csv")
		self.COMPONENT_DIR		= os.path.join(self.BASE_DIR, "xmlcomponents")
		self.CONFIG_DIR			= os.path.join(self.BASE_DIR, "..")
		self.CONFIG_DIR			= os.path.join(self.CONFIG_DIR, "..")
		self.CONFIG_DIR			= os.path.join(self.CONFIG_DIR, "create-data")
		self.CONFIG_DIR			= os.path.join(self.CONFIG_DIR, "config")
		self.CONFIG_FILE		= os.path.join(self.CONFIG_DIR, "config_common.json")
		self.CONFIG_FILE_LOCAL	= os.path.join(self.CONFIG_DIR, "config_migrate_measures_and_quotas.json")

		self.BALANCE_DIR		= os.path.join(self.BASE_DIR, "..")
		self.BALANCE_DIR		= os.path.join(self.BALANCE_DIR, "..")
		self.BALANCE_DIR		= os.path.join(self.BALANCE_DIR, "create-data")
		self.BALANCE_DIR		= os.path.join(self.BALANCE_DIR, "migrate_measures_and_quotas")
		self.BALANCE_DIR		= os.path.join(self.BALANCE_DIR, "source")
		self.BALANCE_DIR		= os.path.join(self.BALANCE_DIR, "quotas")
		self.BALANCE_FILE		= os.path.join(self.BALANCE_DIR, "quota_volume_master.csv")

		# For the word model folders
		self.MODEL_DIR			= os.path.join(self.BASE_DIR, "model")
		self.WORD_DIR			= os.path.join(self.MODEL_DIR, "word")
		self.DOCPROPS_DIR		= os.path.join(self.MODEL_DIR, "docProps")

		# For the output folders
		self.OUTPUT_DIR			= os.path.join(self.BASE_DIR, "output")

		self.get_config()

		# Unless we are running a sequence, find the country code
		if "sequence" in sys.argv[0]:
			return
		else:
			try:
				self.country_profile = sys.argv[1]
			except:
				print ("No country scope parameter found - ending")
				sys.exit()
		
		self.get_country_list()
		self.geo_ids = f.list_to_sql(self.country_codes)

	def create_document(self):
		# Create the quotas table
		my_document = document()
		my_document.get_duties("quotas")
		my_document.get_quota_order_numbers()
		my_document.get_quota_balances_from_csv()
		my_document.get_quota_measures()
		my_document.get_quota_definitions()

		# Create the measures table
		#my_document.has_quotas = False
		self.readTemplates(my_document.has_quotas)
		my_document.get_duties("preferences")

		# Write the document and ZIP it up
		my_document.print_tariffs()
		my_document.print_quotas()
		my_document.create_core()
		my_document.write()
		print ("\nPROCESS COMPLETE - file written to " + my_document.FILENAME + "\n")
			
	def clear(self): 
		# for windows 
		if name == 'nt': 
			_ = system('cls') 
		# for mac and linux(here, os.name is 'posix') 
		else: 
			_ = system('clear')

	def get_config(self):
		# Get global config items
		with open(self.CONFIG_FILE, 'r') as f:
			my_dict = json.load(f)

		self.DBASE					= my_dict['dbase']

		# Get local config items
		with open(self.CONFIG_FILE_LOCAL, 'r') as f:
			my_dict = json.load(f)

		self.all_country_profiles = my_dict['country_profiles']

		# Connect to the database
		self.connect()

	def get_country_list(self):
		try:
			self.country_codes = self.all_country_profiles[self.country_profile]["country_codes"]
		except:
			print ("Country profile does not exist")
			sys.exit()
		self.agreement_name			= self.all_country_profiles[self.country_profile]["agreement_name"]

		self.agreement_date_short	= self.all_country_profiles[self.country_profile]["agreement_date"]
		temp = datetime.strptime(self.agreement_date_short, "%d/%m/%Y")
		self.agreement_date_long	= datetime.strftime(temp, "%d %B %Y").lstrip("0")

		self.table_per_country		= self.all_country_profiles[self.country_profile]["table_per_country"]
		self.version				= self.all_country_profiles[self.country_profile]["version"]
		self.country_name			= self.all_country_profiles[self.country_profile]["country_name"]

	def connect(self):
		self.conn = psycopg2.connect("dbname=" + self.DBASE + " user=postgres password=zanzibar")

	def shutDown(self):
		self.conn.close()

	def get_sections_chapters(self):
		sql = """
		SELECT LEFT(gn.goods_nomenclature_item_id, 2) as chapter, cs.section_id
		FROM chapters_sections cs, goods_nomenclatures gn
		WHERE cs.goods_nomenclature_sid = gn.goods_nomenclature_sid AND gn.producline_suffix = '80'
		ORDER BY 1
		"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows_sections_chapters = cur.fetchall()
		self.section_chapter_list = []
		for rd in rows_sections_chapters:
			sChapter = rd[0]
			iSection = rd[1]
			self.section_chapter_list.append([sChapter, iSection, False])
			
 		# The last parameter is "1" if the chapter equates to a new section
		iLastSection = -1
		for r in self.section_chapter_list:
			iSection = r[1]
			if iSection != iLastSection:
				r[2] = True
			iLastSection = iSection

	def getFootnotes(self):
		# Get all footnotes
		sql = """SELECT DISTINCT fagn.goods_nomenclature_item_id, (fagn.footnote_type || fagn.footnote_id) as footnote, fd.description as footnote_description
		FROM footnote_association_goods_nomenclatures fagn, ml.ml_footnotes fd, footnote_types ft, goods_nomenclatures gn
		WHERE fagn.footnote_id = fd.footnote_id
		AND fagn.footnote_type = fd.footnote_type_id
		AND fagn.footnote_type = ft.footnote_type_id
		AND fagn.goods_nomenclature_item_id = gn.goods_nomenclature_item_id
		AND fagn.productline_suffix = gn.producline_suffix
		AND fagn.productline_suffix = '80'
		AND gn.producline_suffix = '80'
		AND fagn.goods_nomenclature_item_id LIKE '""" + sChapter + """%'
		AND ft.application_code IN ('1', '2')
		AND fagn.validity_start_date < CURRENT_DATE
		AND (fagn.validity_end_date > CURRENT_DATE OR fagn.validity_end_date IS NULL)
		AND gn.validity_start_date < CURRENT_DATE
		AND (gn.validity_end_date > CURRENT_DATE OR gn.validity_end_date IS NULL)
		ORDER BY 1, 2"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows_foonotes = cur.fetchall()
		self.lstFootnotes = list(rows_foonotes)
		self.lstFootnotesUnique = []
		for x in self.lstFootnotes:
			blFound = False
			for y in self.lstFootnotesUnique:
				if x[1] == y[0]:
					blFound = True
					break
			if blFound == False:
				self.lstFootnotesUnique.append([x[1], f.formatFootnote(x[2])])

	def readTemplates(self, has_quotas):
		self.COMPONENT_DIR = os.path.join(self.COMPONENT_DIR, "")
		if has_quotas:
			fDocument = open(os.path.join(self.COMPONENT_DIR, "document_hasquotas.xml"), "r")
		else:
			fDocument = open(os.path.join(self.COMPONENT_DIR, "document_noquotas.xml"), "r")
		self.sDocumentXML = fDocument.read()
		self.sDocumentXML = self.sDocumentXML.replace("{AGREEMENT_NAME}",		self.agreement_name)
		self.sDocumentXML = self.sDocumentXML.replace("{VERSION}",				self.version)
		self.sDocumentXML = self.sDocumentXML.replace("{AGREEMENT_DATE}",		self.agreement_date_long)
		self.sDocumentXML = self.sDocumentXML.replace("{AGREEMENT_DATE_SHORT}",	self.agreement_date_short)
		self.sDocumentXML = self.sDocumentXML.replace("{COUNTRY_NAME}",			self.country_name)

		fFootnoteTable = open(os.path.join(self.COMPONENT_DIR, "table_footnote.xml"), "r") 
		self.sFootnoteTableXML = fFootnoteTable.read()

		fFootnoteTableRow = open(os.path.join(self.COMPONENT_DIR, "tablerow_footnote.xml"), "r") 
		self.sFootnoteTableRowXML = fFootnoteTableRow.read()

		fHeading1 = open(os.path.join(self.COMPONENT_DIR, "heading1.xml"), "r") 
		self.sHeading1XML = fHeading1.read()

		fHeading2 = open(os.path.join(self.COMPONENT_DIR, "heading2.xml"), "r") 
		self.sHeading2XML = fHeading2.read()

		fHeading3 = open(os.path.join(self.COMPONENT_DIR, "heading3.xml"), "r") 
		self.sHeading3XML = fHeading3.read()

		fPara = open(os.path.join(self.COMPONENT_DIR, "paragraph.xml"), "r") 
		self.sParaXML = fPara.read()

		fBullet = open(os.path.join(self.COMPONENT_DIR, "bullet.xml"), "r") 
		self.sBulletXML = fBullet.read()

		fBanner = open(os.path.join(self.COMPONENT_DIR, "banner.xml"), "r") 
		self.sBannerXML = fBanner.read()

		fPageBreak = open(os.path.join(self.COMPONENT_DIR, "pagebreak.xml"), "r") 
		self.sPageBreakXML = fPageBreak.read()

		fTable    = open(os.path.join(self.COMPONENT_DIR, "table_schedule.xml"), "r") 
		fTableRow = open(os.path.join(self.COMPONENT_DIR, "tablerow_schedule.xml"), "r") 

		self.sTableXML = fTable.read()
		self.sTableRowXML = fTableRow.read()

		# Get quota templates
		fQuotaTable    = open(os.path.join(self.COMPONENT_DIR, "table_quota.xml"), "r") 
		fQuotaTableRow = open(os.path.join(self.COMPONENT_DIR, "tablerow_quota.xml"), "r")
		
		self.sQuotaTableXML = fQuotaTable.read()
		self.sQuotaTableRowXML = fQuotaTableRow.read()

		fFootnoteReference = open(os.path.join(self.COMPONENT_DIR, "footnotereference.xml"), "r") 
		self.sFootnoteReferenceXML = fFootnoteReference.read()

		# Footnote templates
		fFootnotes = open(os.path.join(self.COMPONENT_DIR, "footnotes.xml"), "r") 
		self.sFootnotesXML = fFootnotes.read()

		# Horizontal line for putting dividers into the quota table
		fHorizLine = open(os.path.join(self.COMPONENT_DIR, "horiz_line.xml"), "r") 
		self.sHorizLineXML = fHorizLine.read()

		# Soft horizontal line for putting dividers into the quota table
		fHorizLineSoft = open(os.path.join(self.COMPONENT_DIR, "horiz_line_soft.xml"), "r") 
		self.sHorizLineSoftXML = fHorizLineSoft.read()

		# core.xml that contains document information
		fCore = open(os.path.join(self.COMPONENT_DIR, "core.xml"), "r") 
		self.sCoreXML = fCore.read()


	def getSivs(self):
		# Be aware that this is deliberately using old data, meaning that 
		# in reality, the duty charged will be zero
		sql = """SELECT DISTINCT m.goods_nomenclature_item_id
		FROM measures m, measure_conditions mc
		WHERE m.measure_sid = mc.measure_sid
		AND m.validity_start_date > '2018-01-01'
		AND mc.condition_code = 'V'
		ORDER BY m.goods_nomenclature_item_id
		"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for r in rows:
			self.siv_list.append(r[0])
		
		self.siv_list.append("0707000510")
		self.siv_list.append("0707000520")
			
	def getSeasonal(self):
		sFileName = os.path.join(self.SOURCE_DIR, "seasonal_commodities.csv")
		with open(sFileName, "r") as f:
			reader = csv.reader(f)
			temp = list(reader)
		for row in temp:
			commodity_code		= row[0]
			season1_start		= row[1]
			season1_end			= row[2]
			season1_expression	= row[3]
			season2_start		= row[4]
			season2_end			= row[5]
			season2_expression	= row[6]
			season3_start		= row[7]
			season3_end			= row[8]
			season3_expression	= row[9]
			oSeasonal = seasonal(commodity_code, season1_start, season1_end, season1_expression, season2_start, season2_end, season2_expression, season3_start, season3_end, season3_expression)

			self.seasonal_list.append(oSeasonal)

	def getSIVProducts(self):
		# The SQL below gets all products that have a V condition, therefore entry price system against them
		"""SELECT DISTINCT goods_nomenclature_item_id FROM measures m, measure_conditions mc
		WHERE m.measure_sid = mc.measure_sid
		AND mc.condition_code = 'V'
		AND m.validity_start_date >= '2018-01-01' AND (m.validity_end_date <= '2020-01-01' OR m.validity_end_date IS NULL)
		ORDER BY 1"""
		sFileName = os.path.join(self.SOURCE_DIR, "siv_products.csv")
		with open(sFileName, "r") as f:
			reader = csv.reader(f)
			temp = list(reader)
		for i in temp:
			self.siv_list.append(i[0])

	def getCountryAdValoremForSIV(self):
		sql = """SELECT m.goods_nomenclature_item_id, mcc.duty_amount, mcc.duty_expression_id, m.validity_start_date, m.validity_end_date
		FROM measures m, measure_conditions mc, measure_condition_components mcc
		WHERE m.measure_sid = mc.measure_sid
		AND mcc.measure_condition_sid = mc.measure_condition_sid
		AND m.geographical_area_id IN (""" + self.geo_ids + """)
		AND mc.condition_code = 'V'
		AND mcc.duty_expression_id = '01'
		AND validity_start_date <= CURRENT_DATE
		AND (validity_end_date >= CURRENT_DATE OR validity_end_date IS NULL)
		ORDER BY validity_start_date DESC"""
		#print (sql)
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		self.partial_temporary_stops = []
		for rw in rows:
			goods_nomenclature_item_id	= rw[0]
			duty_amount					= rw[1]
			duty_expression_id			= rw[2]
			validity_start_date			= rw[3]
			validity_end_date			= rw[4]

			siv = siv_data(goods_nomenclature_item_id, duty_amount, duty_expression_id, validity_start_date, validity_end_date)
			self.siv_data_list.append (siv)

		# Ensure that there is only one (the latest record listed here; delete all the others)
		unique_siv_data_list_commodities_only	= []
		unique_siv_data_list					= []
		for item in self.siv_data_list:
			if item.goods_nomenclature_item_id not in unique_siv_data_list_commodities_only:
				unique_siv_data_list.append (item)

			unique_siv_data_list_commodities_only.append (item.goods_nomenclature_item_id)

		self.siv_data_list = unique_siv_data_list
		
	def getMeursingProducts(self):
		# The SQL below gets all products that have a V condition, therefore entry price system against them
		"""SELECT DISTINCT goods_nomenclature_item_id FROM measures m, measure_conditions mc
		WHERE m.measure_sid = mc.measure_sid
		AND mc.condition_code = 'V'
		AND m.validity_start_date >= '2018-01-01' AND (m.validity_end_date <= '2020-01-01' OR m.validity_end_date IS NULL)
		ORDER BY 1"""
		sFileName = os.path.join(self.SOURCE_DIR, "meursing_products.csv")
		with open(sFileName, "r") as f:
			reader = csv.reader(f)
			temp = list(reader)
		for i in temp:
			self.meursing_list.append(i[0])

	def getSeasonalProducts(self):
		sFileName = os.path.join(self.SOURCE_DIR, "seasonal_fta_duties.csv")
		with open(sFileName, "r") as f:
			reader = csv.reader(f)
			file = list(reader)

		for row in file:
			goods_nomenclature_item_id	= row[0]
			geographical_area_id		= row[1]
			extent						= row[2]
			duty						= row[3]

			s = seasonal_small(goods_nomenclature_item_id, geographical_area_id, extent, duty)
			self.seasonal_fta_duties.append(s)

