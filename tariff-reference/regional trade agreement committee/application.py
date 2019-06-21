import psycopg2
import sys
import os
from os import system, name 
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
		self.MODEL_DIR			= os.path.join(self.BASE_DIR, "model")
		self.CONFIG_DIR			= os.path.join(self.BASE_DIR, "..")
		self.CONFIG_DIR			= os.path.join(self.CONFIG_DIR, "..")
		self.CONFIG_DIR			= os.path.join(self.CONFIG_DIR, "create-data")
		self.CONFIG_DIR			= os.path.join(self.CONFIG_DIR, "config")
		self.CONFIG_FILE		= os.path.join(self.CONFIG_DIR, "config_common.json")
		self.CONFIG_FILE_LOCAL	= os.path.join(self.CONFIG_DIR, "config_migrate_measures_and_quotas.json")

		self.get_config()
		self.get_suspension_specials()

		# Define the parameters - document type (always schedule)
		self.sDocumentType = "schedule"

		# Define the parameters - start document
		try:
			self.iChapterStart = int(sys.argv[1])
		except:
			self.iChapterStart = 1
			self.iChapterEnd = 99
			
		# Define the parameters - end document
		try:
			self.iChapterEnd   = int(sys.argv[2])
		except:
			self.iChapterEnd   = self.iChapterStart
		if self.iChapterEnd > 99:
			self.iChapterEnd = 99
			
		# Define the parameters - orientation
		self.sOrientation   = ""

		# Define the country profile overlay
		try:
			self.country_profile = sys.argv[3]
		except:
			self.country_profile = ""

		self.format_country_profile()

		self.clear()

	def format_country_profile(self):
		self.country_profile_formatted = self.country_profile.capitalize()

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

		self.DBASE	= my_dict['dbase']
		self.DBASE	= "tariff_staging"
		self.DBASE	= "tariff_eu"
		self.p		= my_dict['p']
		self.reference_authorised_relief_document = my_dict["reference_authorised_relief_document"]

		# Get local config items
		# with open(self.CONFIG_FILE_LOCAL, 'r') as f2:
		# 	my_dict = json.load(f2)
		

		# Connect to the database
		self.connect()

	def connect(self):
		self.conn = psycopg2.connect("dbname=" + self.DBASE + " user=postgres password=" + self.p)

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

	def get_suspension_specials(self):
		self.suspension_specials = []
		self.suspension_specials.append("3814009020")
		self.suspension_specials.append("3814009040")
		self.suspension_specials.append("3814009071")
		self.suspension_specials.append("3814009079")
		self.suspension_specials.append("3814009099")
		self.suspension_specials.append("7019120002")
		self.suspension_specials.append("7019120005")
		self.suspension_specials.append("7019120006")
		self.suspension_specials.append("7019120019")
		self.suspension_specials.append("7019120022")
		self.suspension_specials.append("7019120025")
		self.suspension_specials.append("7019120026")
		self.suspension_specials.append("7019120039")

		self.suspension_specials.append("3824999210")
		self.suspension_specials.append("3824999266")
		self.suspension_specials.append("3824999267")

		self.suspension_specials.append("7019400011")
		self.suspension_specials.append("7019400019")
		self.suspension_specials.append("7019400021")
		self.suspension_specials.append("7019400029")
		self.suspension_specials.append("7019400050")
		self.suspension_specials.append("7019400070")
		
		self.suspension_specials.append("7325991051")
		self.suspension_specials.append("7325991090")

		self.suspension_specials.append("7607119080")
		self.suspension_specials.append("7607119082")
		self.suspension_specials.append("7607119083")

		# NEW
		self.suspension_specials.append("0301919019")
		self.suspension_specials.append("0301919090")
		self.suspension_specials.append("0302118019")
		self.suspension_specials.append("0302118090")
		self.suspension_specials.append("0303149019")
		self.suspension_specials.append("0303149090")
		self.suspension_specials.append("0304429090")
		self.suspension_specials.append("0304829090")
		self.suspension_specials.append("0305430019")
		self.suspension_specials.append("0305430090")
		self.suspension_specials.append("1516209880")
		self.suspension_specials.append("1518009180")
		self.suspension_specials.append("1518009990")
		self.suspension_specials.append("2207100017")
		self.suspension_specials.append("2207100019")
		self.suspension_specials.append("2207100090")
		self.suspension_specials.append("2207200017")
		self.suspension_specials.append("2207200019")
		self.suspension_specials.append("2207200090")
		self.suspension_specials.append("2208909917")
		self.suspension_specials.append("2208909919")
		self.suspension_specials.append("2208909990")
		self.suspension_specials.append("2710122119")
		self.suspension_specials.append("2710122190")
		self.suspension_specials.append("2710122598")
		self.suspension_specials.append("2710122599")
		self.suspension_specials.append("2710123119")
		self.suspension_specials.append("2710123190")
		self.suspension_specials.append("2710124119")
		self.suspension_specials.append("2710124190")
		self.suspension_specials.append("2710124519")
		self.suspension_specials.append("2710124590")
		self.suspension_specials.append("2710124919")
		self.suspension_specials.append("2710124990")
		self.suspension_specials.append("2710125019")
		self.suspension_specials.append("2710125090")
		self.suspension_specials.append("2710127019")
		self.suspension_specials.append("2710127090")
		self.suspension_specials.append("2710129019")
		self.suspension_specials.append("2710129090")
		self.suspension_specials.append("3102290090")
		self.suspension_specials.append("3102600090")
		self.suspension_specials.append("3102900090")
		self.suspension_specials.append("3105100090")
		self.suspension_specials.append("3105201090")
		self.suspension_specials.append("3105510090")
		self.suspension_specials.append("3105590090")
		self.suspension_specials.append("3105902090")
		self.suspension_specials.append("3814001017")
		self.suspension_specials.append("3814001090")
		self.suspension_specials.append("3814009079")
		self.suspension_specials.append("3814009099")
		self.suspension_specials.append("3820000019")
		self.suspension_specials.append("3820000090")
		self.suspension_specials.append("3824999245")
		self.suspension_specials.append("3824999250")
		self.suspension_specials.append("3824999253")
		self.suspension_specials.append("3824999267")
		self.suspension_specials.append("3824999299")
		self.suspension_specials.append("3824999277")
		self.suspension_specials.append("3824999285")
		self.suspension_specials.append("3824999287")
		self.suspension_specials.append("3824999289")
		self.suspension_specials.append("3826001020")
		self.suspension_specials.append("3826001029")
		self.suspension_specials.append("3826001059")
		self.suspension_specials.append("3826001099")
		self.suspension_specials.append("3826001050")
		self.suspension_specials.append("3826009090")
		self.suspension_specials.append("3924900090")
		self.suspension_specials.append("4012120090")
		self.suspension_specials.append("6911100010")
		self.suspension_specials.append("6912002119")
		self.suspension_specials.append("6912002199")
		self.suspension_specials.append("6912002390")
		self.suspension_specials.append("7323930090")
		self.suspension_specials.append("7323990090")
		self.suspension_specials.append("7325100010")
		self.suspension_specials.append("7325100015")
		self.suspension_specials.append("7325100020")
		self.suspension_specials.append("7325100099")
		self.suspension_specials.append("7325991035")
		self.suspension_specials.append("7325991040")
		self.suspension_specials.append("7325991090")
		self.suspension_specials.append("7607111190")
		self.suspension_specials.append("7607191090")
		self.suspension_specials.append("8516797090")
		self.suspension_specials.append("8516900060")
		self.suspension_specials.append("8516900099")
		self.suspension_specials.append("8708701080")
		self.suspension_specials.append("8708701085")
		self.suspension_specials.append("8708705080")
		self.suspension_specials.append("8708705085")
		self.suspension_specials.append("7019120019")
		self.suspension_specials.append("7019120006")
		# END NEW		


	def getAuthorisedUse(self):
		if self.reference_authorised_relief_document != 0:
			sql = """SELECT DISTINCT goods_nomenclature_item_id FROM ml.v5_2019 m WHERE measure_type_id = '105' ORDER BY 1;"""
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
