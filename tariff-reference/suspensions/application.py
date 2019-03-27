import psycopg2
import sys
import os, re
from os import system, name 
import csv
import json
import codecs
from datetime import datetime

import functions as f
from commodity import commodity
from commodity import davidowen_commodity

from duty import duty
from progressbar import ProgressBar
from hierarchy import hierarchy
from hierarchy import subheading_hierarchy

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
		self.suspensions_xml		= ""
		self.david_owen_list		= []
		
		self.partial_temporary_stops	= []

		self.BASE_DIR			= os.path.dirname(os.path.abspath(__file__))
		self.SOURCE_DIR			= os.path.join(self.BASE_DIR, "source")
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

		arg1 = ""
		self.include_do_only = False
		try:
			arg1 = sys.argv[1].strip()
		except:
			arg1 = ""
		if arg1 != "":
			self.include_do_only = True
		

		self.get_config()
		self.readTemplates()

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
		self.p		= my_dict['p']

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
		self.agreement_date_long	= datetime.strftime(temp, "%d %B %Y")

		self.table_per_country		= self.all_country_profiles[self.country_profile]["table_per_country"]
		self.version				= self.all_country_profiles[self.country_profile]["version"]
		self.country_name			= self.all_country_profiles[self.country_profile]["country_name"]

	def connect(self):
		self.conn = psycopg2.connect("dbname=" + self.DBASE + " user=postgres password" + self.p)

	def shutDown(self):
		self.conn.close()

	def getSectionsChapters(self):
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

	def readTemplates(self):
		self.COMPONENT_DIR = os.path.join(self.COMPONENT_DIR, "")

		file = open(os.path.join(self.COMPONENT_DIR, "document.xml"), "r")
		self.sDocumentXML = file.read()

		file = open(os.path.join(self.COMPONENT_DIR, "tablerow.xml"), "r")
		self.sTableRowXML = file.read()

		file = open(os.path.join(self.COMPONENT_DIR, "tier1.xml"), "r")
		self.sTier1XML = file.read()

		file = open(os.path.join(self.COMPONENT_DIR, "tier2.xml"), "r")
		self.sTier2XML = file.read()

		file = open(os.path.join(self.COMPONENT_DIR, "tier3.xml"), "r")
		self.sTier3XML = file.read()

		file = open(os.path.join(self.COMPONENT_DIR, "tier4.xml"), "r")
		self.sTier4XML = file.read()

		file = open(os.path.join(self.COMPONENT_DIR, "tier5.xml"), "r")
		self.sTier5XML = file.read()

		file = open(os.path.join(self.COMPONENT_DIR, "tier6.xml"), "r")
		self.sTier6XML = file.read()

		file = open(os.path.join(self.COMPONENT_DIR, "tier7.xml"), "r")
		self.sTier7XML = file.read()


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

	def getPartialTemporaryStops(self, quota_order_number_list):
		sql = """
		SELECT m.ordernumber, m.measure_sid, mpts.validity_start_date, mpts.validity_end_date
		FROM measure_partial_temporary_stops mpts, measures m
		WHERE mpts.measure_sid = m.measure_sid
		AND m.ordernumber is not null
		AND mpts.validity_start_date < '2019-03-30' AND (mpts.validity_end_date >= '2019-03-30' OR mpts.validity_end_date IS NULL)
		AND m.ordernumber IN (""" + quota_order_number_list + """) 
		ORDER BY 1, 4 DESC
		"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		self.partial_temporary_stops = []
		for rw in rows:
			quota_order_number_id	= rw[0]
			measure_sid				= rw[1]
			validity_start_date		= rw[2]
			validity_end_date		= rw[3]
			pts = partial_temporary_stop(quota_order_number_id, measure_sid, validity_start_date, validity_end_date)
			self.partial_temporary_stops.append (pts)

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
		

	def get_suspensions(self):
		sql = """
		SELECT measure_sid, goods_nomenclature_item_id, validity_start_date FROM ml.v5
		WHERE measure_type_id IN ('112', '115') AND regulation_id = 'R182069'
		ORDER BY goods_nomenclature_item_id
		/*LIMIT 500*/
		"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		self.commodity_list = []
		for row in rows:
			measure_sid					= row[0]
			goods_nomenclature_item_id	= row[1]
			validity_start_date			= row[2]
			my_commodity = commodity(measure_sid, goods_nomenclature_item_id, validity_start_date)
			self.commodity_list.append(my_commodity)

		sql = """
		SELECT mc.measure_sid, mc.duty_expression_id, mc.duty_amount, mc.monetary_unit_code, measurement_unit_code,
		measurement_unit_qualifier_code, m.goods_nomenclature_item_id
		FROM measure_components mc, ml.v5 m
		WHERE m.measure_sid = mc.measure_sid
		AND m.measure_type_id IN ('112', '115') AND m.regulation_id = 'R182069'
		ORDER BY m.goods_nomenclature_item_id, duty_expression_id
		"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		#self.shutDown()

		self.duty_list = []
		for row in rows:
			measure_sid						= row[0]
			duty_expression_id				= row[1]
			duty_amount						= row[2]
			monetary_unit_code				= row[3]
			measurement_unit_code			= row[4]
			measurement_unit_qualifier_code	= row[5]
			goods_nomenclature_item_id		= row[6]

			my_duty = duty(goods_nomenclature_item_id, "", "", "", duty_expression_id, duty_amount, monetary_unit_code, measurement_unit_code, measurement_unit_qualifier_code, measure_sid)
			self.duty_list.append(my_duty)


		for my_commodity in self.commodity_list:
			for my_duty in self.duty_list:
				if my_duty.measure_sid == my_commodity.measure_sid:
					my_commodity.duty_list.append(my_duty)
					#break

		print ("Combining duties")
		for my_commodity in self.commodity_list:
			my_commodity.combineDuties()

		subheading_list = []
		for my_commodity in self.commodity_list:
			subheading_list.append(my_commodity.subheading)
		
		print("Getting subheading hierarchies")
		self.list_of_hierarchies = []
		my_set = set(subheading_list)
		p = ProgressBar(len(my_set), sys.stdout)
		cnt = 1
		for subheading in my_set:
			obj_hierarchy = self.get_hierarchy(subheading)

			p.print_progress(cnt)
			cnt +=1
			obj_subheading_hierarchy = subheading_hierarchy(subheading, obj_hierarchy)
			self.list_of_hierarchies.append(obj_subheading_hierarchy)



		print("\n\nWriting XML for Word document")
		p = ProgressBar(len(self.commodity_list), sys.stdout)
		cnt = 1
		self.table_xml = ""
		for my_commodity in self.commodity_list:
			if my_commodity.include:
				my_commodity.get_hierarchy()
				row_xml = self.sTableRowXML
				row_xml = row_xml.replace("[COMMODITY_CODE]", 	my_commodity.goods_nomenclature_item_id)
				row_xml = row_xml.replace("[DUTY_EXPRESSION]",	my_commodity.combined_duty)
				row_xml = row_xml.replace("[END_DATE]", 		my_commodity.end_date)
				row_xml = row_xml.replace("[DESCRIPTION]", 		my_commodity.hierarchy)
				self.table_xml += row_xml

			p.print_progress(cnt)
			cnt +=1

		self.cleanse_xml()
		
		self.suspensions_xml = self.sDocumentXML
		self.suspensions_xml = self.suspensions_xml.replace("[TABLE_CONTENT]", self.table_xml)

	def get_hierarchy(self, subheading):
		sql = """
		SELECT goods_nomenclature_item_id, producline_suffix, number_indents, description
		FROM ml.goods_nomenclature_export3('""" + subheading + """%')
		ORDER BY goods_nomenclature_item_id, producline_suffix
		"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		hierarchy_list = []

		for row in rows:
			goods_nomenclature_item_id	= row[0]
			producline_suffix			= row[1]
			number_indents				= row[2]
			description					= row[3]
			my_hierarchy = hierarchy(goods_nomenclature_item_id, producline_suffix, number_indents, description)
			hierarchy_list.append(my_hierarchy)
		return hierarchy_list

	def cleanse_xml(self):
		self.table_xml = re.sub("<w:t>(.*)m2</w:t>", "<w:t>\g<1>m</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"superscript\"/></w:rPr><w:t>2</w:t>", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("<w:t>(.*)m3</w:t>", "<w:t>\g<1>m</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"superscript\"/></w:rPr><w:t>3</w:t>", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("<w:t>(.*)K2O</w:t>", "<w:t>\g<1>K</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>2</w:t></w:r><w:r><w:t>O</w:t>", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("<w:t>(.*)H2O2</w:t>", "<w:t>\g<1>H</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>2</w:t></w:r><w:r><w:t>O</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>2</w:t>", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("<w:t>(.*)P2O5</w:t>", "<w:t>\g<1>P</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>2</w:t></w:r><w:r><w:t>O</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>5</w:t>", self.table_xml, flags=re.MULTILINE)
		
		# Subscripts
		self.table_xml = re.sub("@(.)", '</w:t></w:r><w:r><w:rPr><w:vertAlign w:val="subscript"/></w:rPr><w:t>\\1</w:t></w:r><w:r><w:t>', self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("\$(.)", '</w:t></w:r><w:r><w:rPr><w:vertAlign w:val="superscript"/></w:rPr><w:t>\\1 </w:t></w:r><w:r><w:t>', self.table_xml, flags=re.MULTILINE)

		# Missing commas
		self.table_xml = re.sub("([0-9]),([0-9]) kg", "\\1.\\2 kg", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]) Kg", "\\1.\\2 kg", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]) C", "\\1.\\2 C", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9])kg", "\\1.\\2kg", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) g", "\\1.\\2 g", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3})g", "\\1.\\2g", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) dl", "\\1.\\2 dl", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) m", "\\1.\\2 m", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3})m", "\\1.\\2m", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) decitex", "\\1.\\2 decitex", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) l", "\\1.\\2 l", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) kW", "\\1.\\2 kW", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) W", "\\1.\\2 W", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) V", "\\1.\\2 V", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) Ah", "\\1.\\2 Ah", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) bar", "\\1.\\2 bar", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) cm", "\\1.\\2 cm", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) Nm", "\\1.\\2 Nm", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) kV", "\\1.\\2 kV", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) kHz", "\\1.\\2 kHz", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) kV", "\\1.\\2 kV", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) MHz", "\\1.\\2 MHz", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) μm", "\\1.\\2 μm", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) Ohm", "\\1.\\2 Ohm", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) dB", "\\1.\\2 dB", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("([0-9]),([0-9]{1,3}) kvar", "\\1.\\2 kvar", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("±([0-9]),([0-9]{1,3})", "±\\1.\\2", self.table_xml, flags=re.MULTILINE)
		self.table_xml = re.sub("€ ([0-9]{1,3}),([0-9]{1,3})", "€ \\1.\\2", self.table_xml, flags=re.MULTILINE)
		self.table_xml = self.table_xml.replace(" %", "%")



	def write_file(self):
		basedir = os.path.dirname(os.path.abspath(__file__))
		sFileName = basedir + "\\model\\word\\document.xml"
		file = codecs.open(sFileName, "w", "utf-8")
		file.write(self.suspensions_xml)
		file.close() 

		###########################################################################
		## Finally, ZIP everything up
		###########################################################################
		if self.include_do_only:
			self.word_filename = "suspensions_python_do_only.docx"
		else:
			self.word_filename = "suspensions_python.docx"
		f.zipdir(self.word_filename)

	def get_DavidOwen_list(self):
		sFileName = os.path.join(self.SOURCE_DIR, "david_owen_excel.csv")
		with open(sFileName, "r") as f:
			reader = csv.reader(f)
			temp = list(reader)
		for i in temp:
			goods_nomenclature_item_id	= i[0]
			duty_expression				= i[1]
			end_date					= i[2]
			obj_do = davidowen_commodity(goods_nomenclature_item_id, duty_expression, end_date)
			self.david_owen_list.append(obj_do)
