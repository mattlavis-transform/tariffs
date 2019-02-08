import psycopg2
import sys
import os
import csv
import json

import functions
from seasonal import seasonal
from special import special

class application(object):
	def __init__(self):
		self.siv_list               = []
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

		self.BASE_DIR			= os.path.dirname(os.path.abspath(__file__))
		self.SOURCE_DIR			= os.path.join(self.BASE_DIR, "source")
		self.COMPONENT_DIR		= os.path.join(self.BASE_DIR, "xmlcomponents")
		self.CONFIG_DIR			= os.path.join(self.BASE_DIR, "..")
		self.CONFIG_DIR			= os.path.join(self.CONFIG_DIR, "..")
		self.CONFIG_DIR			= os.path.join(self.CONFIG_DIR, "create-data")
		self.CONFIG_DIR			= os.path.join(self.CONFIG_DIR, "config")
		self.CONFIG_FILE		= os.path.join(self.CONFIG_DIR, "config_common.json")
		self.CONFIG_FILE_LOCAL	= os.path.join(self.CONFIG_DIR, "config_migrate_measures_and_quotas.json")

		self.get_config()

		# Define the parameters - document type
		try:
			self.sDocumentType = sys.argv[1]
			if self.sDocumentType == "s":
				self.sDocumentType = "schedule"
			if self.sDocumentType == "c":
				self.sDocumentType = "classification"
		except:
			self.sDocumentType = "schedule"

		# Define the parameters - start document
		try:
			self.iChapterStart = int(sys.argv[2])
		except:
			self.iChapterStart = 1
			self.iChapterEnd = 99
			
		# Define the parameters - end document
		try:
			self.iChapterEnd   = int(sys.argv[3])
		except:
			self.iChapterEnd   = self.iChapterStart
		if self.iChapterEnd > 99:
			self.iChapterEnd = 99
			
		# Define the parameters - orientation
		try:
			self.sOrientation   = sys.argv[4]
		except:
			self.sOrientation   = ""

		if (self.sDocumentType != "classification" and self.sDocumentType != "schedule"):
			self.sDocumentType = "schedule"

	def get_config(self):
		# Get global config items
		with open(self.CONFIG_FILE, 'r') as f:
			my_dict = json.load(f)

		self.DBASE					= my_dict['dbase']

		# Get local config items
		#with open(self.CONFIG_FILE_LOCAL, 'r') as f2:
		#	my_dict = json.load(f2)
		#self.import_file_list = my_dict["import_files"]

		# Connect to the database
		self.connect()

	def connect(self):
		self.conn = psycopg2.connect("dbname=" + self.DBASE + " user=postgres password=zanzibar")

	def shutDown(self):
		self.conn.close()


	def getSectionsChapters(self):
		sql = """
		SELECT LEFT(gn.goods_nomenclature_item_id, 2) as chapter, cs.section_id
		FROM chapters_sections cs, goods_nomenclatures gn
		WHERE cs.goods_nomenclature_sid = gn.goods_nomenclature_sid
		AND gn.producline_suffix = '80'
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
				self.lstFootnotesUnique.append([x[1], functions.formatFootnote(x[2])])

	def readTemplates(self):
		self.COMPONENT_DIR = os.path.join(self.COMPONENT_DIR, "")

		# Main document templates
		if self.sDocumentType == "classification":
			fDocument = open(os.path.join(self.COMPONENT_DIR, "document_classification.xml"), "r")
		else:
			if self.sOrientation == "landscape":
				fDocument = open(os.path.join(self.COMPONENT_DIR, "document_schedule_landscape.xml"), "r")
			else:
				fDocument = open(os.path.join(self.COMPONENT_DIR, "document_schedule.xml"), "r")
		self.sDocumentXML = fDocument.read()

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

		if (self.sDocumentType == "classification"):
			fTable    = open(os.path.join(self.COMPONENT_DIR, "table_classification.xml"), "r") 
			fTableRow = open(os.path.join(self.COMPONENT_DIR, "tablerow_classification.xml"), "r") 
		else:
			if self.sOrientation == "landscape":
				fTable    = open(os.path.join(self.COMPONENT_DIR, "table_schedule_landscape.xml"), "r") 
				fTableRow = open(os.path.join(self.COMPONENT_DIR, "tablerow_schedule_landscape.xml"), "r") 
			else:
				fTable    = open(os.path.join(self.COMPONENT_DIR, "table_schedule.xml"), "r") 
				fTableRow = open(os.path.join(self.COMPONENT_DIR, "tablerow_schedule.xml"), "r") 

		self.sTableXML = fTable.read()
		self.sTableRowXML = fTableRow.read()

		fFootnoteReference = open(os.path.join(self.COMPONENT_DIR, "footnotereference.xml"), "r") 
		self.sFootnoteReferenceXML = fFootnoteReference.read()

		# Footnote templates
		fFootnotes = open(os.path.join(self.COMPONENT_DIR, "footnotes.xml"), "r") 
		self.sFootnotesXML = fFootnotes.read()


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
			
	def getVessels(self):
		sql = """SELECT DISTINCT goods_nomenclature_item_id FROM ml.v5_brexit_day m WHERE measure_type_id = '117';"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for r in rows:
			self.vessels_list.append(r[0])

	def getCivilAir(self):
		sql = """SELECT DISTINCT gn.goods_nomenclature_item_id
		FROM goods_nomenclature_descriptions gnd, goods_nomenclatures gn
		WHERE gn.goods_nomenclature_item_id = gnd.goods_nomenclature_item_id
		AND (LOWER(description) LIKE '%civil air%' OR LOWER(description) LIKE '%civil use%')
		AND gn.validity_start_date <= '2019/01/01'
		AND (gn.validity_end_date >= '2019/03/29' OR gn.validity_end_date IS NULL) ORDER BY 1"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for r in rows:
			self.civilair_list.append(r[0])

		"""
		sFileName = os.path.join(self.SOURCE_DIR, "civilair_commodities.csv")
		with open(sFileName, "r") as f:
			reader = csv.reader(f)
			temp = list(reader)
		for i in temp:
			self.civilair_list.append(i[0])
		"""

	def getAirworthiness(self):
		sql = """SELECT DISTINCT goods_nomenclature_item_id FROM ml.v5_brexit_day m WHERE measure_type_id = '119';"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for r in rows:
			self.airworthiness_list.append(r[0])

	def getAircraft(self):
		sql = """SELECT DISTINCT goods_nomenclature_item_id FROM ml.v5_brexit_day m WHERE measure_type_id = '115' AND regulation_id = 'R953050' ORDER BY 1;"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for r in rows:
			self.aircraft_list.append(r[0])

	def getPharmaceuticals(self):
		sql = """SELECT DISTINCT goods_nomenclature_item_id FROM ml.v5_brexit_day m WHERE additional_code_type_id = '2' AND additional_code_id = '500' ORDER BY 1;"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for r in rows:
			self.pharmaceuticals_list.append(r[0])

	def getITAProducts(self):
		sFileName = os.path.join(self.SOURCE_DIR, "ita_commodities.csv")
		with open(sFileName, "r") as f:
			reader = csv.reader(f)
			temp = list(reader)
		for i in temp:
			self.ita_list.append(i[0])

	def getGeneralRelief(self):
		sFileName = os.path.join(self.SOURCE_DIR, "generalrelief_commodities.csv")
		with open(sFileName, "r") as f:
			reader = csv.reader(f)
			temp = list(reader)
		for i in temp:
			self.generalrelief_list.append(i[0])

	def getAuthorisedUse(self):
		sql = """SELECT DISTINCT goods_nomenclature_item_id FROM ml.v5_2019 m WHERE measure_type_id = '105';"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for r in rows:
			self.authoriseduse_list.append(r[0])
		
		# Also add in cucumbers: the data cannot find these, therefore manually added
		self.authoriseduse_list.append("0707000510")
		self.authoriseduse_list.append("0707000520")
		
	def getSpecials(self):
		sFileName = os.path.join(self.SOURCE_DIR, "special_notes.csv")
		with open(sFileName, "r") as f:
			reader = csv.reader(f)
			temp = list(reader)
		for row in temp:
			commodity_code	= row[0]
			note			= row[1]
			oSpecial = special(commodity_code, note)

			self.special_list.append(oSpecial)

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
