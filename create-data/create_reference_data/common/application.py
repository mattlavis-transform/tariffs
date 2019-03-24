import psycopg2
import sys
import os
from os import system, name
import csv
import re
import codecs
import json
import xmlschema

#import functions as f
from common.footnote import footnote
from common.certificate import certificate
from common.base_regulation import base_regulation
import common.functions as fn

class application(object):
	def __init__(self):
		self.clear()

		self.BASE_DIR			= os.path.join(os.path.dirname( __file__ ), '..')
		temp					= os.path.join(self.BASE_DIR, '..')
		temp					= os.path.join(temp, 'convert_and_import_taric')
		self.OUT_DIR			= os.path.join(temp, "xml_out")
		self.OUT_DIR			= os.path.join(temp, "xml_out")
		self.TEMPLATE_DIR		= os.path.join(self.BASE_DIR, "templates")
		self.SCHEMA_DIR			= os.path.join(self.BASE_DIR, "xsd")
		self.SOURCE_DIR			= os.path.join(self.BASE_DIR, "source")
		self.CONFIG_DIR			= os.path.join(self.BASE_DIR, "..")
		self.CONFIG_DIR			= os.path.join(self.CONFIG_DIR, "config")
		self.CONFIG_FILE		= os.path.join(self.CONFIG_DIR, "config_common.json")
		self.CONFIG_FILE_LOCAL	= os.path.join(self.CONFIG_DIR, "config_create_reference_data.json")

		# The XML export directory
		temp				= os.path.join(self.BASE_DIR, '..')
		temp				= os.path.join(temp, 'convert_and_import_taric')
		self.XML_DIR		= os.path.join(temp, "xml_in")
		self.XML_DIR		= os.path.join(self.XML_DIR, "custom")

		self.footnotes_list				= []
		self.footnote_type_list			= []
		self.measure_type_list			= []
		self.additional_code_type_list	= []
		self.goods_nomenclature_list	= []
		self.certificate_type_list		= []
		self.geographical_area_list		= []
		self.membership_list			= []
		self.certificates_list			= []
		self.base_regulations_list		= []
		self.regulation_groups_list		= []
		self.cnt = 0

		self.base_footnote_description_period_sid			= 200000
		self.base_certificate_description_period_sid 		= 10000
		self.base_geographical_area_description_period_sid	= 10000

		self.base_envelope_id = 5000
		self.message_id = 1
		self.fname = ""

		self.get_config()
		self.get_minimum_sids()
		self.transaction_id = self.last_transaction_id

	def get_minimum_sids(self):
		with open(self.CONFIG_FILE, 'r') as f:
			my_dict = json.load(f)
		
		min_list = my_dict['minimum_sids']

		self.last_additional_code_description_period_sid	= self.larger(self.get_scalar("SELECT MAX(additional_code_description_period_sid) FROM additional_code_description_periods_oplog;"), min_list['additional.code.description.periods']) + 1
		self.last_additional_code_sid						= self.larger(self.get_scalar("SELECT MAX(additional_code_sid) FROM additional_codes_oplog;"), min_list['additional.codes']) + 1

		self.last_certificate_description_period_sid		= self.larger(self.get_scalar("SELECT MAX(certificate_description_period_sid) FROM certificate_description_periods_oplog;"), min_list['certificate.description.periods']) + 1
		self.last_footnote_description_period_sid			= self.larger(self.get_scalar("SELECT MAX(footnote_description_period_sid) FROM footnote_description_periods_oplog;"), min_list['footnote.description.periods']) + 1
		self.last_geographical_area_description_period_sid	= self.larger(self.get_scalar("SELECT MAX(geographical_area_description_period_sid) FROM geographical_area_description_periods_oplog;"), min_list['geographical.area.description.periods']) + 1
		self.last_geographical_area_sid						= self.larger(self.get_scalar("SELECT MAX(geographical_area_sid) FROM geographical_areas_oplog;"), min_list['geographical.areas']) + 1

		self.last_goods_nomenclature_sid					= self.larger(self.get_scalar("SELECT MAX(goods_nomenclature_sid) FROM goods_nomenclatures_oplog;"), min_list['goods.nomenclature']) + 1
		self.last_goods_nomenclature_indent_sid				= self.larger(self.get_scalar("SELECT MAX(goods_nomenclature_indent_sid) FROM goods_nomenclature_indents_oplog;"), min_list['goods.nomenclature.indents']) + 1
		self.last_goods_nomenclature_description_period_sid	= self.larger(self.get_scalar("SELECT MAX(goods_nomenclature_description_period_sid) FROM goods_nomenclature_description_periods_oplog;"), min_list['goods.nomenclature.description.periods']) + 1

		self.last_measure_sid								= self.larger(self.get_scalar("SELECT MAX(measure_sid) FROM measures_oplog;"), min_list['measures']) + 1
		self.last_measure_condition_sid						= self.larger(self.get_scalar("SELECT MAX(measure_condition_sid) FROM measure_conditions_oplog"), min_list['measure.conditions']) + 1

		self.last_quota_order_number_sid					= self.larger(self.get_scalar("SELECT MAX(quota_order_number_sid) FROM quota_order_numbers_oplog"), min_list['quota.order.numbers']) + 1
		self.last_quota_order_number_origin_sid				= self.larger(self.get_scalar("SELECT MAX(quota_order_number_origin_sid) FROM quota_order_number_origins_oplog"), min_list['quota.order.number.origins']) + 1
		self.last_quota_definition_sid						= self.larger(self.get_scalar("SELECT MAX(quota_definition_sid) FROM quota_definitions_oplog"), min_list['quota.definitions']) + 1
		self.last_quota_suspension_period_sid				= self.larger(self.get_scalar("SELECT MAX(quota_suspension_period_sid) FROM quota_suspension_periods_oplog"), min_list['quota.suspension.periods']) + 1
		self.last_quota_blocking_period_sid					= self.larger(self.get_scalar("SELECT MAX(quota_blocking_period_sid) FROM quota_blocking_periods_oplog"), min_list['quota.blocking.periods']) + 1

	def validate(self, filename):
		self.d ("Validating XML file", False)
		schema_path = os.path.join(self.SCHEMA_DIR, "envelope.xsd")
		my_schema = xmlschema.XMLSchema(schema_path)
		try:
			if my_schema.is_valid(filename):
				self.d ("The file validated successfully")
			else:
				self.d ("The file did not validate")
		except:
			self.d ("The file did not validate and crashed the validator")

	def larger(self, a, b):
		if a > b:
			return a
		else:
			return b

	def get_scalar(self, sql):
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		#l = list(rows)
		return (rows[0][0])


	def get_profile(self, profile_type):
		if profile_type == "regulations":
			self.d("Getting regulation profile")
			if (len(sys.argv) > 1):
				profile = sys.argv[1]
				self.d("Using regulation profile: " + profile)
				try:
					with open(self.CONFIG_FILE_LOCAL, 'r') as f:
						my_dict = json.load(f)

					self.excel_source	= os.path.join(self.SOURCE_DIR, my_dict["regulation_profiles"][profile]["source"])
					self.xml_file		= my_dict["regulation_profiles"][profile]["dest"]

				except:
					self.d("No profile specified or profile not found. Please supply correct profile name after the script name.", False)
					sys.exit()

	def set_config(self):
		jsonFile = open(self.CONFIG_FILE, "r")	# Open the JSON file for reading
		data = json.load(jsonFile)				# Read the JSON into the buffer
		jsonFile.close()						# Close the JSON file

		data["last_transaction_id"] = self.transaction_id

		jsonFile = open(self.CONFIG_FILE, "w+")
		jsonFile.write(json.dumps(data, indent=4, sort_keys=True))
		jsonFile.close()

	def set_config2(self, key, value):
		jsonFile = open(self.CONFIG_FILE, "r")	# Open the JSON file for reading
		data = json.load(jsonFile)				# Read the JSON into the buffer
		jsonFile.close()						# Close the JSON file

		data["minimum_sids"][key] = value

		jsonFile = open(self.CONFIG_FILE, "w+")
		jsonFile.write(json.dumps(data, indent=4, sort_keys=True))
		jsonFile.close()

	def get_config(self):
		with open(self.CONFIG_FILE, 'r') as f:
			my_dict = json.load(f)

		self.last_transaction_id	= my_dict['last_transaction_id']
		self.DBASE					= my_dict['dbase']
		#self.DBASE = "tariff_eu"
		#print (self.DBASE)
		#sys.exit()
		self.debug					= my_dict['debug']
		self.connect()

	def d(self, s, include_indent = True):
		if self.debug:
			if include_indent:
				s = "- " + s
			else:
				s = "\n" + s.upper()
			#print (s + "\n")
			print (s)

	def clear(self):
		# for windows
		if name == 'nt':
			_ = system('cls')
		# for mac and linux(here, os.name is 'posix')
		else:
			_ = system('clear')

	def connect(self):
		self.conn = psycopg2.connect("dbname=" + self.DBASE + " user=postgres password=zanzibar")

	def getTemplates(self):
		# Get envelope XML
		filename = os.path.join(self.TEMPLATE_DIR, "envelope.xml")
		handle = open(filename, "r")
		self.envelope_XML = handle.read()

		# Get footnote type description update XML
		filename = os.path.join(self.TEMPLATE_DIR, "footnote.type.description.update.xml")
		handle = open(filename, "r")
		self.update_footnote_type_description_XML = handle.read()

		# Get footnote type description update XML
		filename = os.path.join(self.TEMPLATE_DIR, "footnote.type.update.xml")
		handle = open(filename, "r")
		self.update_footnote_type_XML = handle.read()

		# Get certificate type insert XML
		filename = os.path.join(self.TEMPLATE_DIR, "certificate.type.insert.xml")
		handle = open(filename, "r")
		self.insert_certificate_type_XML = handle.read()

		# Get certificate type description update XML
		filename = os.path.join(self.TEMPLATE_DIR, "certificate.type.description.update.xml")
		handle = open(filename, "r")
		self.update_certificate_type_description_XML = handle.read()

		# Get footnote type insert XML
		filename = os.path.join(self.TEMPLATE_DIR, "footnote.type.insert.xml")
		handle = open(filename, "r")
		self.insert_footnote_type_XML = handle.read()

		# Get footnote description update XML
		filename = os.path.join(self.TEMPLATE_DIR, "footnote.description.update.xml")
		handle = open(filename, "r")
		self.update_footnote_description_XML = handle.read()

		# Get measure type insert XML
		filename = os.path.join(self.TEMPLATE_DIR, "measure.type.insert.xml")
		handle = open(filename, "r")
		self.insert_measure_type_XML = handle.read()

		# Get measure description update XML
		filename = os.path.join(self.TEMPLATE_DIR, "measure.type.description.update.xml")
		handle = open(filename, "r")
		self.update_measure_type_description_XML = handle.read()

		# Get footnote insert XML
		filename = os.path.join(self.TEMPLATE_DIR, "footnote.insert.xml")
		handle = open(filename, "r")
		self.insert_footnote_XML = handle.read()

		# Get additional code type description update XML
		filename = os.path.join(self.TEMPLATE_DIR, "additional.code.type.description.update.xml")
		handle = open(filename, "r")
		self.update_additional_code_description_XML = handle.read()

		# Get additional code type insert XML
		filename = os.path.join(self.TEMPLATE_DIR, "additional.code.type.insert.xml")
		handle = open(filename, "r")
		self.insert_additional_code_description_XML = handle.read()

		# Get geographical area description update XML
		filename = os.path.join(self.TEMPLATE_DIR, "geographical.area.description.update.xml")
		handle = open(filename, "r")
		self.update_geographical_area_description_XML = handle.read()

		# Get geographical area insert XML
		filename = os.path.join(self.TEMPLATE_DIR, "geographical.area.insert.xml")
		handle = open(filename, "r")
		self.insert_geographical_area_XML = handle.read()

		# Get certificate insert XML
		filename = os.path.join(self.TEMPLATE_DIR, "certificate.insert.xml")
		handle = open(filename, "r")
		self.insert_certificate_XML = handle.read()

		# Get certificate description update XML
		filename = os.path.join(self.TEMPLATE_DIR, "certificate.description.update.xml")
		handle = open(filename, "r")
		self.update_certificate_description_XML = handle.read()

		# Get base regulation insert XML
		filename = os.path.join(self.TEMPLATE_DIR, "base.regulation.insert.xml")
		handle = open(filename, "r")
		self.insert_base_regulation_XML = handle.read()

		# Get base regulation update XML
		filename = os.path.join(self.TEMPLATE_DIR, "base.regulation.update.xml")
		handle = open(filename, "r")
		self.update_base_regulation_XML = handle.read()

		# Get regulation group insert XML
		filename = os.path.join(self.TEMPLATE_DIR, "regulation.group.insert.xml")
		handle = open(filename, "r")
		self.insert_regulation_group_XML = handle.read()

		# Get regulation group update XML
		filename = os.path.join(self.TEMPLATE_DIR, "regulation.group.update.xml")
		handle = open(filename, "r")
		self.update_regulation_group_XML = handle.read()

		# Get goods nomenclature description update XML
		filename = os.path.join(self.TEMPLATE_DIR, "goods.nomenclature.description.update.xml")
		handle = open(filename, "r")
		self.update_goods_nomenclature_description_XML = handle.read()

		# Get memberships XML
		filename = os.path.join(self.TEMPLATE_DIR, "membership.xml")
		handle = open(filename, "r")
		self.membership_XML = handle.read()

	def writeResults(self):
		t_in = ""
		t_out = ""
		for oF in self.footnotes_list:
			t_in += oF.description + "\n"
			t_out += oF.new_description + "\n"
		fname = os.path.join(self.OUT_DIR, "out.txt")
		f3 = open(fname, "w", encoding="utf-8")
		f3.write(t_out)
		f3.close()

		fname = os.path.join(self.OUT_DIR, "in.txt")
		f3 = open(fname, "w", encoding="utf-8")
		f3.write(t_in)
		f3.close()
		#sys.exit()

	def getFoonotes(self):
		self.connect()
		sql = """
		SELECT DISTINCT f.footnote_type_id, f.footnote_id, f.description, f.validity_start_date, f.validity_end_date
		FROM ml.ml_footnotes f, footnote_association_measures fam, ml.v5_2019 m
		WHERE f.footnote_id = fam.footnote_id AND f.footnote_type_id = fam.footnote_type_id
		AND  fam.measure_sid = m.measure_sid
		AND f.national IS NULL AND m.national IS NULL

		UNION

		SELECT DISTINCT f.footnote_type_id, f.footnote_id, f.description, f.validity_start_date, f.validity_end_date
		FROM ml.ml_footnotes f, footnote_association_goods_nomenclatures fagn, ml.v5_2019 m
		WHERE f.footnote_id = fagn.footnote_id AND f.footnote_type_id = fagn.footnote_type
		AND fagn.goods_nomenclature_item_id = m.goods_nomenclature_item_id
		AND f.national IS NULL AND m.national IS NULL

		ORDER BY 1, 2
		"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for r in rows:
			footnote_type_id = fn.mstr(r[0])
			footnote_id = fn.mstr(r[1])
			description = fn.mstr(r[2])
			f = footnote(footnote_type_id, footnote_id, "", description, "")
			self.footnotes_list.append(f)


	def getCertificates(self):
		self.connect()
		sql = """
		SELECT DISTINCT c.certificate_type_code, c.certificate_code, c.description
		FROM ml.ml_certificate_codes c, ml.v5_2019 m, measure_conditions mc
		WHERE m.measure_sid = mc.measure_sid
		AND mc.certificate_type_code = c.certificate_type_code
		AND mc.certificate_code = c.certificate_code
		ORDER BY 1, 2
		"""
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for r in rows:
			certificate_type_code = fn.mstr(r[0])
			certificate_code = fn.mstr(r[1])
			description = fn.mstr(r[2])
			f = certificate(certificate_type_code, certificate_code, "", description, "")
			self.certificates_list.append(f)

	def resolveFootnotes(self):
		i = 1
		for oF in self.footnotes_list:
			oF.resolve(self)
			i += 1
