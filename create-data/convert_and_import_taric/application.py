import xml.etree.ElementTree as ET
import xmlschema
import psycopg2
import sys
import os
from os import system, name 
import csv
import re
import json
import codecs
import uuid 
import hashlib
import subprocess

from datetime import datetime
from log import log

from common.regulation import regulation

from profile.profile_10000_footnote_type							import profile_10000_footnote_type
from profile.profile_10005_footnote_type_description				import profile_10005_footnote_type_description
from profile.profile_11000_certificate_type							import profile_11000_certificate_type
from profile.profile_11005_certificate_type_description				import profile_11005_certificate_type_description
from profile.profile_12000_additional_code_type						import profile_12000_additional_code_type
from profile.profile_12005_additional_code_type_description			import profile_12005_additional_code_type_description
from profile.profile_14000_measure_type_series						import profile_14000_measure_type_series
from profile.profile_14005_measure_type_series_description			import profile_14005_measure_type_series_description
from profile.profile_15000_regulation_group							import profile_15000_regulation_group
from profile.profile_15005_regulation_group_description				import profile_15005_regulation_group_description
from profile.profile_16000_regulation_role_type						import profile_16000_regulation_role_type
from profile.profile_16005_regulation_role_type_description			import profile_16005_regulation_role_type_description
from profile.profile_17000_publication_sigle						import profile_17000_publication_sigle
from profile.profile_20000_footnote									import profile_20000_footnote
from profile.profile_20005_footnote_description_period				import profile_20005_footnote_description_period
from profile.profile_20010_footnote_description						import profile_20010_footnote_description
from profile.profile_20500_certificate								import profile_20500_certificate
from profile.profile_20505_certificate_description_period			import profile_20505_certificate_description_period
from profile.profile_20510_certificate_description					import profile_20510_certificate_description
from profile.profile_21000_measurement_unit							import profile_21000_measurement_unit
from profile.profile_21005_measurement_unit_description				import profile_21005_measurement_unit_description
from profile.profile_21500_measurement_unit_qualifier				import profile_21500_measurement_unit_qualifier
from profile.profile_21505_measurement_unit_qualifier_description	import profile_21505_measurement_unit_qualifier_description
from profile.profile_22000_measurement								import profile_22000_measurement
from profile.profile_22500_monetary_unit							import profile_22500_monetary_unit
from profile.profile_22505_monetary_unit_description				import profile_22505_monetary_unit_description
from profile.profile_23000_duty_expression							import profile_23000_duty_expression
from profile.profile_23005_duty_expression_description				import profile_23005_duty_expression_description
from profile.profile_23500_measure_type								import profile_23500_measure_type
from profile.profile_23505_measure_type_description					import profile_23505_measure_type_description
from profile.profile_24000_additional_code_type_measure_type		import profile_24000_additional_code_type_measure_type
from profile.profile_24500_additional_code							import profile_24500_additional_code
from profile.profile_24505_additional_code_description_period		import profile_24505_additional_code_description_period
from profile.profile_24510_additional_code_description				import profile_24510_additional_code_description
from profile.profile_25000_geographical_area						import profile_25000_geographical_area
from profile.profile_25005_geographical_area_description_period		import profile_25005_geographical_area_description_period
from profile.profile_25010_geographical_area_description			import profile_25010_geographical_area_description
from profile.profile_25015_geographical_area_membership				import profile_25015_geographical_area_membership
from profile.profile_27500_complete_abrogation_regulation			import profile_27500_complete_abrogation_regulation
from profile.profile_28000_explicit_abrogation_regulation			import profile_28000_explicit_abrogation_regulation
from profile.profile_28500_base_regulation							import profile_28500_base_regulation
from profile.profile_29000_modification_regulation					import profile_29000_modification_regulation
from profile.profile_29500_prorogation_regulation					import profile_29500_prorogation_regulation
from profile.profile_29505_prorogation_regulation_action			import profile_29505_prorogation_regulation_action
from profile.profile_30000_full_temporary_stop_regulation			import profile_30000_full_temporary_stop_regulation
from profile.profile_30500_regulation_replacement					import profile_30500_regulation_replacement
from profile.profile_35000_measure_condition_code					import profile_35000_measure_condition_code
from profile.profile_35005_measure_condition_code_description		import profile_35005_measure_condition_code_description
from profile.profile_35500_measure_action							import profile_35500_measure_action
from profile.profile_35505_measure_action_description				import profile_35505_measure_action_description

from profile.profile_36000_quota_order_number						import profile_36000_quota_order_number
from profile.profile_36010_quota_order_number_origin				import profile_36010_quota_order_number_origin
from profile.profile_36015_quota_order_number_origin_exclusion		import profile_36015_quota_order_number_origin_exclusion

from profile.profile_37000_quota_definition							import profile_37000_quota_definition
from profile.profile_37005_quota_association						import profile_37005_quota_association
from profile.profile_37010_quota_blocking_period					import profile_37010_quota_blocking_period
from profile.profile_37015_quota_suspension_period					import profile_37015_quota_suspension_period

from profile.profile_37500_quota_balance_event						import profile_37500_quota_balance_event
from profile.profile_37505_quota_unblocking_event					import profile_37505_quota_unblocking_event
from profile.profile_37510_quota_critical_event						import profile_37510_quota_critical_event
from profile.profile_37515_quota_exhaustion_event					import profile_37515_quota_exhaustion_event
from profile.profile_37520_quota_reopening_event					import profile_37520_quota_reopening_event
from profile.profile_37525_quota_unsuspension_event					import profile_37525_quota_unsuspension_event
from profile.profile_37530_quota_closed_and_balance_transferred_event	import profile_37530_quota_closed_and_balance_transferred_event


from profile.profile_40000_goods_nomenclature						import profile_40000_goods_nomenclature
from profile.profile_40005_goods_nomenclature_indent				import profile_40005_goods_nomenclature_indent
from profile.profile_40010_goods_nomenclature_description_period	import profile_40010_goods_nomenclature_description_period
from profile.profile_40015_goods_nomenclature_description			import profile_40015_goods_nomenclature_description
from profile.profile_40020_footnote_association_goods_nomenclature	import profile_40020_footnote_association_goods_nomenclature
from profile.profile_40035_goods_nomenclature_origin				import profile_40035_goods_nomenclature_origin
from profile.profile_40040_goods_nomenclature_successor				import profile_40040_goods_nomenclature_successor

from profile.profile_43000_measure									import profile_43000_measure
from profile.profile_43005_measure_component						import profile_43005_measure_component
from profile.profile_43010_measure_condition						import profile_43010_measure_condition
from profile.profile_43011_measure_condition_component				import profile_43011_measure_condition_component
from profile.profile_43015_measure_excluded_geographical_area		import profile_43015_measure_excluded_geographical_area
from profile.profile_43020_footnote_association_measure				import profile_43020_footnote_association_measure
from profile.profile_43025_measure_partial_temporary_stop			import profile_43025_measure_partial_temporary_stop

from profile.profile_44000_monetary_exchange_period					import profile_44000_monetary_exchange_period
from profile.profile_44005_monetary_exchange_rate					import profile_44005_monetary_exchange_rate

class application(object):
	def __init__(self):
		self.clear()

		self.BASE_DIR			= os.path.dirname(os.path.abspath(__file__))
		self.SCHEMA_DIR			= os.path.join(self.BASE_DIR,	"xsd")
		self.TEMPLATE_DIR		= os.path.join(self.BASE_DIR,	"templates")
		self.XML_IN_DIR			= os.path.join(self.BASE_DIR,	"xml_in")
		self.IMPORT_DIR			= os.path.join(self.BASE_DIR,	"import")
		self.XML_OUT_DIR		= os.path.join(self.BASE_DIR,	"xml_out")
		self.TEMP_DIR			= os.path.join(self.BASE_DIR,	"temp")
		self.TEMP_FILE			= os.path.join(self.TEMP_DIR,	"temp.xml")
		self.LOG_DIR			= os.path.join(self.BASE_DIR,	"log")
		self.IMPORT_LOG_DIR		= os.path.join(self.LOG_DIR,	"import")
		self.REG_LOG_DIR		= os.path.join(self.LOG_DIR,	"regulation")
		
		self.LOG_FILE								= os.path.join(self.LOG_DIR,	"log.csv")
		self.LOG_FILE_MEASURE						= os.path.join(self.LOG_DIR,	"log_measure_deleted.csv")
		self.LOG_FILE_MEASURE_COMPONENT				= os.path.join(self.LOG_DIR,	"log_measure_component_deleted.csv")
		self.LOG_FILE_MEASURE_CONDITION				= os.path.join(self.LOG_DIR,	"log_measure_condition_deleted.csv")
		self.LOG_FILE_MEASURE_CONDITION_COMPONENT	= os.path.join(self.LOG_DIR,	"log_measure_condition_component_deleted.csv")

		self.MERGE_DIR			= os.path.join(self.XML_IN_DIR,	"custom")
		self.DUMP_DIR			= os.path.join(self.BASE_DIR,	"dump")
		self.CONFIG_DIR			= os.path.join(self.BASE_DIR, "..")
		self.CONFIG_DIR			= os.path.join(self.CONFIG_DIR, "config")
		self.CONFIG_FILE		= os.path.join(self.CONFIG_DIR, "config_common.json")
		self.CONFIG_FILE_LOCAL	= os.path.join(self.CONFIG_DIR, "config_convert_and_import_taric_files.json")

		self.IMPORT_PROFILE_DIR	= os.path.join(self.CONFIG_DIR, "import_profile")

		self.namespaces 				= {'oub': 'urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0', 'env': 'urn:publicid:-:DGTAXUD:GENERAL:ENVELOPE:1.0', } # add more as needed
		self.envelope_id				= ""
		self.sDivider					= ""
		self.message_id					= 1
		self.debug		    			= True
		self.simple_filenames			= True
		self.remove_futures				= True
		self.abrogation_regulation_id	= "I1900030" # Used for abrogating the PTS records that need truncating on Brexit day

		self.correlation_id				= ""
		self.checksum					= ""
		self.filesize					= ""
		self.source_file_name			= ""

		self.log_list_string			= []
		self.log_list					= []

		my_script = sys.argv[0]
		self.get_config()
		self.get_minimum_sids()

		if self.DBASE == "tariff_eu":
			self.IMPORT_DIR			= self.XML_IN_DIR
		else:
			self.IMPORT_DIR			= self.IMPORT_DIR


		# Read in the whole of the log file, so that we can compare
		# current actions against past actions that have already been made
		with open(self.LOG_FILE) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter = ",")
			for row in csv_reader:
				s = log(row[0], row[1], row[2], row[3], row[4], row[5])
				self.log_list.append (s)
				s2 = row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + row[4] + "," + row[5]
				self.log_list_string.append (s2)

	def get_config(self):
		# Get global config items
		with open(self.CONFIG_FILE, 'r') as f:
			my_dict = json.load(f)
		critical_date = my_dict['critical_date']
		self.critical_date	= datetime.strptime(critical_date, '%Y-%m-%d')
		self.DBASE			= my_dict['dbase']
		self.p				= my_dict['p']
		
		my_script = sys.argv[0]
		if my_script == "import_dev.py":
			self.DBASE = "tariff_dev"
		elif my_script == "import_staging.py":
			self.DBASE = "tariff_staging"
		elif my_script == "import_cds.py":
			self.DBASE = "tariff_cds"
		elif my_script == "import_eu.py":
			self.DBASE = "tariff_eu"


		# Get local config items
		with open(self.CONFIG_FILE_LOCAL, 'r') as f2:
			my_dict = json.load(f2)
		self.import_file_list = my_dict["import_files"]

		# Connect to the database
		self.connect()


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


	def endDateEUMeasures(self, xml_file, sMerge1 = "", sMerge2 = "", sMerge3 = "", sMerge4 = "", sMerge5 = "", sMerge6 = "", sMerge7 = "", sMerge8 = "", sMerge9 = "", sMerge10 = ""):
		self.convertFilename(xml_file)
		self.d("Creating converted file for " + self.output_filename, False)

		self.xml_file_In	= os.path.join(self.XML_IN_DIR,  xml_file)
		self.xml_file_Out	= os.path.join(self.XML_OUT_DIR, self.output_filename)

		# Load file
		ET.register_namespace('oub', 'urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0')
		ET.register_namespace('env', 'urn:publicid:-:DGTAXUD:GENERAL:ENVELOPE:1.0')
		tree = ET.parse(self.xml_file_In)
		root = tree.getroot()

		# Get the envelope ID
		self.envelope_id = root.get("id")
		if (len(self.envelope_id)) == 5:
			self.envelope_id = self.envelope_id[0:2] + "0" + self.envelope_id[2:]
			root.set("id", self.envelope_id)

		# Loop through the transactions, looking for items to delete or amend
		quota_order_number_origin_list	= []
		quota_order_definition_list		= []
		measure_list					= []
		measure_condition_list			= []
		action_list = ["update", "delete", "insert"]
		self.regulation_log_filename	= os.path.join(self.REG_LOG_DIR, "reg_log_" + xml_file.replace("xml", "csv"))
		self.regulation_list = []
		self.new_regulation_list = []

		if self.remove_futures:
			for oTransaction in root.findall('.//env:transaction', self.namespaces):
				for oMessage in oTransaction.findall('.//env:app.message', self.namespaces):
					record_code			= oMessage.find(".//oub:record.code", self.namespaces).text
					sub_record_code		= oMessage.find(".//oub:subrecord.code", self.namespaces).text
					update_type			= oMessage.find(".//oub:update.type", self.namespaces).text
					update_type_string	= action_list[int(update_type) - 1]
					
					# 27500	COMPLETE ABROGATION REGULATIONS - Delete everything
					if record_code == "275" and sub_record_code == "00": # and update_type == "3":
						#regulation_id		= self.getValue(oMessage, ".//oub:base.regulation.id")
						#information_text	= self.getValue(oMessage, ".//oub:information.text")
						#reg = regulation(regulation_id, information_text, "base")
						#self.new_regulation_list.append(reg)
						oTransaction.remove (oMessage)

					# 28000	EXPLICIT ABROGATION REGULATIONS - Delete everything
					if record_code == "280" and sub_record_code == "00": # and update_type == "3":
						#regulation_id		= self.getValue(oMessage, ".//oub:base.regulation.id")
						#information_text	= self.getValue(oMessage, ".//oub:information.text")
						#reg = regulation(regulation_id, information_text, "base")
						#self.new_regulation_list.append(reg)
						oTransaction.remove (oMessage)

					# 28500	BASE REGULATIONS - Now delete all of these
					if record_code == "285" and sub_record_code == "00": # and update_type == "3":
						regulation_id		= self.getValue(oMessage, ".//oub:base.regulation.id")
						information_text	= self.getValue(oMessage, ".//oub:information.text")
						reg = regulation(regulation_id, information_text, "base")
						#self.new_regulation_list.append(reg)
						oTransaction.remove (oMessage)

					# 29000	MODIFICATION REGULATIONS - Now delete all of these
					if record_code == "290" and sub_record_code == "00": # and update_type == "3":
						regulation_id		= self.getValue(oMessage, ".//oub:modification.regulation.id")
						information_text	= self.getValue(oMessage, ".//oub:information.text")
						reg = regulation(regulation_id, information_text, "modification")
						#self.new_regulation_list.append(reg)
						oTransaction.remove (oMessage)

					# 29500	PROROGATION REGULATIONS - Now delete all of these
					if record_code == "295" and sub_record_code == "00": # and update_type == "3":
						regulation_id		= self.getValue(oMessage, ".//oub:prorogation.regulation.id")
						information_text	= self.getValue(oMessage, ".//oub:information.text")
						reg = regulation(regulation_id, information_text, "prorogation")
						#self.new_regulation_list.append(reg)
						oTransaction.remove (oMessage)

					# 30000	FULL TEMPORARY STOP REGULATIONS - Now delete all of these
					if record_code == "300" and sub_record_code == "00": # and update_type == "3":
						#regulation_id		= self.getValue(oMessage, ".//oub:prorogation.regulation.id")
						#information_text	= self.getValue(oMessage, ".//oub:information.text")
						#reg = regulation(regulation_id, information_text, "prorogation")
						#self.new_regulation_list.append(reg)
						oTransaction.remove (oMessage)

					# 30500	REGULATION REPLACEMENTS - Now delete all of these
					if record_code == "305" and sub_record_code == "00": # and update_type == "3":
						#regulation_id		= self.getValue(oMessage, ".//oub:prorogation.regulation.id")
						#information_text	= self.getValue(oMessage, ".//oub:information.text")
						#reg = regulation(regulation_id, information_text, "prorogation")
						#self.new_regulation_list.append(reg)
						oTransaction.remove (oMessage)

					# 36000	QUOTA ORDER NUMBER
					# We will always be loading quota order numbers
					amend_quota_order_numbers = False
					if amend_quota_order_numbers == True:
						if record_code == "360" and sub_record_code == "00" and update_type in ("1", "3"):
							validity_start_date	= self.getDateValue(oMessage, ".//oub:validity.start.date")
							# Action - remove the quota order number node if the quota does not start until after the critical date
							# Note - it does not matter if the quota order number straddles the critical date - we can leave it in place
							quota_order_number_sid =  self.getValue(oMessage, ".//quota.order.number.sid")
							if validity_start_date > self.critical_date:
								oTransaction.remove (oMessage)
								self.register_update("360", "00", "delete", update_type_string, quota_order_number_sid, xml_file, "Delete instruction to create a new quota order number (" + quota_order_number_sid + ") after the critical date")

					# 36010	QUOTA ORDER NUMBER ORIGIN
					# We will always be loading quota order origins
					if amend_quota_order_numbers == True:
						if record_code == "360" and sub_record_code == "10" and update_type in ("1", "3"):
							validity_start_date	= self.getDateValue(oMessage, ".//oub:validity.start.date")
							validity_end_date	= self.getDateValue(oMessage, ".//oub:validity.end.date")
							
							# Action - remove the quota order number origin message node
							# if the quota order number origin does not start until after the critical date
							if validity_start_date >= self.critical_date:
								sid = self.getValue(oMessage, ".//oub:quota.order.number.origin.sid")
								quota_order_number_origin_list.append(sid)
								oTransaction.remove (oMessage)
								self.register_update("360", "10", "delete", update_type_string, sid, xml_file, "Delete instruction to create quota order number origin " + sid)
							else:
								pass
								# Action - insert the end date on the quota order number origin if the end date is blank
								# I do not believe this is necessary, hence commented out
								"""
								if validity_end_date == "":
									self.register_update("360", "10", "update", update_type_string, sid, xml_file, "Insert an end date for a quota order number origin which was otherwise un-end dated for origin " + sid)
									oElement = self.getNode(oMessage, ".//oub:quota.order.number.origin")
									self.add_edit_node(oElement, "oub:validity.end.date", "oub:validity.start.date", datetime.strftime(self.critical_date, "%Y-%m-%d"))
								"""
								# Action - update the end date if the end date is later than the critical date
								# Likewise, I do not believe this is necessary, hence commented out
								"""
								elif validity_end_date >= self.critical_date:
									oElement = self.getNode(oMessage, ".//oub:quota.order.number.origin")
									self.d("Update an existing quota order number end date to the critical date")
									self.setNode(oElement, "oub:validity.end.date", datetime.strftime(self.critical_date, "%Y-%m-%d"))
								"""

					# 37000	QUOTA DEFINITION
					# We actually do want to delete quota definitions
					if record_code == "370" and sub_record_code == "00" and update_type in ("1", "3"):
						validity_start_date		= self.getDateValue(oMessage, ".//oub:validity.start.date")
						validity_end_date		= self.getDateValue(oMessage, ".//oub:validity.end.date")
						quota_definition_sid	=  self.getValue(oMessage, ".//oub:quota.definition.sid")
						
						# Action - remove the quota definition message node if the quota definition does not start
						# until after the critical date
						if validity_start_date >= self.critical_date:
							quota_order_definition_list.append (quota_definition_sid)
							oTransaction.remove (oMessage)
							self.register_update("370", "00", "delete", update_type_string, quota_definition_sid, xml_file, "Delete instruction to create quota order definition " + quota_definition_sid)
						else:
							# Action - insert the end date on the quota definition, if the end date is blank
							# Not sure if this is possible, but here for completion
							if validity_end_date == "":
								oElement = self.getNode(oMessage, ".//oub:quota.definition")
								self.add_edit_node(oElement, "oub:validity.end.date", "oub:validity.start.date", datetime.strftime(self.critical_date, "%Y-%m-%d"))
								self.register_update("370", "00", "update", update_type_string, quota_definition_sid, xml_file, "Insert an end date for a quota definition which was otherwise un-end dated for definition " + quota_definition_sid)
							
							# Action - update the end date, if the end date is later than the critical date
							# and the start date is before the critical date, i.e. straddles
							elif validity_end_date >= self.critical_date:
								oElement = self.getNode(oMessage, ".//oub:quota.definition")
								self.setNode(oElement, "oub:validity.end.date", datetime.strftime(self.critical_date, "%Y-%m-%d"))
								self.register_update("370", "00", "update", update_type_string, quota_definition_sid, xml_file, "Update an explicit quota definition end date to the critical date for quota definition " + quota_definition_sid)

					# 43000	MEASURE
					measure_count = 0
					if record_code == "430": #  and sub_record_code == "00":
						oTransaction.remove (oMessage)

					"""
					if record_code == "430" and sub_record_code == "00":
						measure_count += 1
						validity_start_date					= self.getDateValue(oMessage, ".//oub:validity.start.date")
						validity_end_date					= self.getDateValue(oMessage, ".//oub:validity.end.date")
						measure_generating_regulation_role	= self.getValue(oMessage, ".//oub:measure.generating.regulation.role")
						measure_generating_regulation_id	= self.getValue(oMessage, ".//oub:measure.generating.regulation.id")
						measure_type_id						= self.getValue(oMessage, ".//oub:measure.type")
						self.regulation_list.append (measure_generating_regulation_id)
						#print (measure_type_id)

						# Action - remove the message node if the measure does not start until after the critical date
						measure_sid =  self.getValue(oMessage, ".//oub:measure.sid")
						if update_type in ("1", "3"):
							if validity_start_date > self.critical_date:
								oTransaction.remove (oMessage)
								measure_list.append(measure_sid)
								self.register_update("430", "00", "delete", update_type_string, measure_sid, xml_file, "Delete instruction for measure that would have started after EU Exit with measure.sid of " + measure_sid)
							
							# Action - if the measure begins before EU Exit, but the end date is empty,
							# then insert an end date (i.e the critical date - to be determined)
							# This also requires a justification regulation ID and role to be added
							elif validity_end_date == "":
								oElement = self.getNode(oMessage, ".//oub:measure")

								self.add_edit_node(oElement, "oub:justification.regulation.id", "oub:measure.generating.regulation.id", measure_generating_regulation_id)
								self.add_edit_node(oElement, "oub:justification.regulation.role", "oub:measure.generating.regulation.id", measure_generating_regulation_role)
								self.add_edit_node(oElement, "oub:validity.end.date", "oub:measure.generating.regulation.id", datetime.strftime(self.critical_date, "%Y-%m-%d"))

								self.register_update("430", "00", "update", update_type_string, measure_sid, xml_file, "Update a measure with no end date to end on the critical date - measure_sid " + measure_sid)
							
							# Action - if the measure begins before EU Exit, but the end date is after EU Exit and is fixed,
							# then alter the end date to be the critical date - to be determined)
							elif validity_end_date >= self.critical_date:
								oElement = self.getNode(oMessage, ".//oub:measure")
								self.setNode(oElement, "oub:validity.end.date", datetime.strftime(self.critical_date, "%Y-%m-%d"))
								self.add_edit_node(oElement, "oub:justification.regulation.id",   "oub:validity.end.date", measure_generating_regulation_id)
								self.add_edit_node(oElement, "oub:justification.regulation.role", "oub:validity.end.date", measure_generating_regulation_role)
								
								self.register_update("430", "00", "update", update_type_string, measure_sid, xml_file, "Update a measure that starts before EU Exit and ends after EU Exit to end on the critical date - measure_sid: " + measure_sid)


					# 43025	MEASURE PARTIAL TEMPORARY STOP
					if record_code == "430" and sub_record_code == "25" # and update_type in ("1", "3"):
						oElement = self.getNode(oMessage, ".//oub:measure.partial.temporary.stop")
						validity_start_date	= self.getDateValue(oMessage, ".//oub:validity.start.date")
						validity_end_date	= self.getDateValue(oMessage, ".//oub:validity.end.date")
						measure_sid =  self.getValue(oMessage, ".//oub:measure.sid")

						# Action - remove the message node if the measure PTS does not start until after the critical date
						if validity_start_date > self.critical_date:
							oTransaction.remove (oMessage)
							self.register_update("430", "25", "delete", update_type_string, measure_sid, xml_file, "Delete instruction for partial temporary stop beginning after EU Exit with measure.sid of " + measure_sid)

						# Action - if there is no formal end date on a PTS, then Insert the end date
						# as well as the abrogation.regulation.id
						elif validity_end_date == "":
							self.add_edit_node(oElement, "oub:validity.end.date",		 "oub:validity.start.date", datetime.strftime(self.critical_date, "%Y-%m-%d"))
							self.add_edit_node(oElement, "oub:abrogation.regulation.id", "oub:partial.temporary.stop.regulation.officialjournal.page", self.abrogation_regulation_id)
							self.register_update("430", "25", "delete", update_type_string, measure_sid, xml_file, "End date a partial temporary stop beginning before EU Exit with no end date measure.sid of " + measure_sid)
					"""

			########################################## PHASE 2 ########################################
			# Second loop through the transactions = needed once the list variables have been populated
			# Loop through the transactions, looking for items to delete or amend
			for oTransaction in root.findall('.//env:transaction', self.namespaces):
				for oMessage in oTransaction.findall('.//env:app.message', self.namespaces):
					record_code			= oMessage.find(".//oub:record.code", self.namespaces).text
					sub_record_code		= oMessage.find(".//oub:subrecord.code", self.namespaces).text
					update_type			= oMessage.find(".//oub:update.type", self.namespaces).text
					update_type_string	= action_list[int(update_type) - 1]

					if 1 > 2:
						# 36015	QUOTA ORDER NUMBER EXCLUSION
						# Search for quota order number origin exclusions
						# If found in the same file, where they match to a quota order number origin that has been removed,
						# then remove the quota order number origin exclusion
						if record_code == "360" and sub_record_code == "15" and update_type in ("1", "3"):
							removed_node = False
							quota_order_number_origin_sid = oMessage.find(".//oub:quota.order.number.origin.sid", self.namespaces).text
							for sid in quota_order_number_origin_list:
								if (sid == quota_order_number_origin_sid):
									oTransaction.remove (oMessage)
									self.register_update("360", "15", "delete", update_type_string, sid, xml_file, "Delete quota order number origin exclusion with quota definition: " + sid)
									break

							# If found in the log file, where they match to a quota order number origin that has been removed,
							# then remove the quota order number origin exclusion
							if not(removed_node):
								for s in self.log_list:
									if s.record_code == "360" and s.sub_record_code == "10" and (s.update_type_string in ("insert", "update")):
										if s.sid == quota_order_number_origin_sid:
											oTransaction.remove (oMessage)
											self.register_update("360", "15", "delete", update_type_string, sid, xml_file, "Delete quota order number origin exclusion with quota definition: " + s.sid)
											break


					if 1 > 0:
						# Additional action needed - will need to look for any quota associations and events for any definitions
						# that have been stripped, and get rid of them too
						# 37005	QUOTA ASSOCIATION
						if record_code == "370" and sub_record_code == "05" and update_type in ("1", "3"):
							main_quota_definition_sid	= self.getValue(oMessage, ".//oub:main.quota.definition.sid")
							sub_quota_definition_sid	= self.getValue(oMessage, ".//oub:sub.quota.definition.sid")
							for sid in quota_order_definition_list:
								if (main_quota_definition_sid == sid) or (sub_quota_definition_sid == sid):
									oTransaction.remove (oMessage)
									self.register_update("370", "05", "delete", update_type_string, sid, xml_file, "Delete quota association with quota definition: " + sid)
									break

						# 37010	QUOTA BLOCKING PERIOD
						if record_code == "370" and sub_record_code == "10" and update_type in ("1", "3"):
							quota_blocking_period_sid	= self.getValue(oMessage, ".//oub:quota.blocking.period.sid")
							quota_definition_sid		= self.getValue(oMessage, ".//oub:quota.definition.sid")
							blocking_start_date			= self.getDateValue(oMessage, ".//oub:blocking.start.date")
							blocking_end_date			= self.getDateValue(oMessage, ".//oub:blocking.end.date")

							# Action - Delete a blocking period if the blocking period starts after the critical date
							if blocking_start_date > self.critical_date:
								oTransaction.remove (oMessage)
								self.register_update("370", "10", "delete", update_type_string, quota_blocking_period_sid, xml_file, "Delete quota blocking period with quota definition " + quota_definition_sid + " and blocking period SID of " + quota_blocking_period_sid)

							# Action - If the blocking period starts before the critical date, but ends after the critical date
							# then end date the blocking period on the critical date
							# Please note - blocking periods must have an end date, so there is no condition where end date is blank
							elif blocking_start_date < self.critical_date and blocking_end_date > self.critical_date:
								oElement = self.getNode(oMessage, ".//oub:quota.blocking.period")
								self.register_update("370", "10", "update", update_type_string, quota_blocking_period_sid, xml_file, "Update an existing blocking period end date to the critical date")
								self.setNode(oElement, "oub:blocking.end.date", datetime.strftime(self.critical_date, "%Y-%m-%d"))

							# Action - search through this file's quota definitions and look for any items that have been deleted
							# If the quota definition has been deleted, then delete the blocking period too
							for sid in quota_order_definition_list:
								if (quota_definition_sid == sid):
									try:
										oTransaction.remove (oMessage)
										self.register_update("370", "10", "delete", update_type_string, quota_blocking_period_sid, xml_file, "Delete quota blocking period " + update_type_string + " instruction")
									except:
										pass
									break

						# 37015	QUOTA SUSPENSION PERIOD
						if record_code == "370" and sub_record_code == "15" and update_type in ("1", "3"):
							quota_suspension_period_sid	= self.getValue(oMessage, ".//oub:quota.suspension.period.sid")
							quota_definition_sid		= self.getValue(oMessage, ".//oub:quota.definition.sid")
							suspension_start_date		= self.getDateValue(oMessage, ".//oub:suspension.start.date")
							suspension_end_date			= self.getDateValue(oMessage, ".//oub:suspension.end.date")

							# Action - Delete a suspension period if the suspension period starts after the critical date
							if suspension_start_date > self.critical_date:
								oTransaction.remove (oMessage)
								self.register_update("370", "15", "delete", update_type_string, quota_suspension_period_sid, xml_file, "Delete quota suspension period with quota definition " + quota_definition_sid + " and suspension period SID of " + quota_suspension_period_sid)

							# Action - If the suspension period starts before the critical date, but ends after the critical date
							# then end date the suspension period on the critical date
							# Please note - suspension periods must have an end date, so there is no condition where end date is blank
							elif suspension_start_date < self.critical_date and suspension_end_date > self.critical_date:
								oElement = self.getNode(oMessage, ".//oub:quota.suspension.period")
								self.d("Update an existing suspension period end date to the critical date")
								self.setNode(oElement, "oub:suspension.end.date", datetime.strftime(self.critical_date, "%Y-%m-%d"))
								self.register_update("370", "15", "update", update_type_string, quota_suspension_period_sid, xml_file, "Update an existing suspension period end date to the critical date")

							# Action - search through this file's quota definitions and look for any items that have been deleted
							# If the quota definition has been deleted, then delete the suspension period too
							for sid in quota_order_definition_list:
								if (quota_definition_sid == sid):
									try:
										oTransaction.remove (oMessage)
										self.register_update("370", "15", "delete", update_type_string, quota_suspension_period_sid, xml_file, "Delete quota suspension period with quota definition: " + sid)
									except:
										pass
									break

						# 37505	QUOTA UNBLOCKING EVENT
						if record_code == "375" and sub_record_code == "05" and update_type in ("1", "3"):
							quota_definition_sid		= self.getValue(oMessage, ".//oub:quota.definition.sid")
							unblocking_date				= self.getDateValue(oMessage, ".//oub:unblocking.date")

							# Action - Delete an unblocking event if it takes place after the critical date
							if unblocking_date > self.critical_date:
								oTransaction.remove (oMessage)
								self.register_update("375", "05", "delete", update_type_string, quota_definition_sid, xml_file, "Delete quota unblocking event with quota definition " + quota_definition_sid)

							# Action - search through this file's quota definitions and look for any items that have been deleted
							# If the quota definition has been deleted, then delete the suspension period too
							for sid in quota_order_definition_list:
								if (quota_definition_sid == sid):
									try:
										self.register_update("375", "05", "delete", update_type_string, quota_definition_sid, xml_file, "Delete quota unblocking event with quota definition: " + sid)
										oTransaction.remove (oMessage)
									except:
										pass
									break

						# 37510	QUOTA CRITICAL EVENT
						if record_code == "375" and sub_record_code == "10" and update_type in ("1", "3"):
							quota_definition_sid		= self.getValue(oMessage, ".//oub:quota.definition.sid")
							critical_state_change_date	= self.getDateValue(oMessage, ".//oub:critical.state.change.date")

							# Action - Delete an critical event if it takes place after the critical date
							if critical_state_change_date > self.critical_date:
								oTransaction.remove (oMessage)
								self.register_update("375", "10", "delete", update_type_string, quota_definition_sid, xml_file, "Delete quota critical event with quota definition " + quota_definition_sid)

							# Action - search through this file's quota definitions and look for any items that have been deleted
							# If the quota definition has been deleted, then delete the suspension period too
							for sid in quota_order_definition_list:
								if (quota_definition_sid == sid):
									try:
										oTransaction.remove (oMessage)
										self.register_update("375", "10", "delete", update_type_string, quota_definition_sid, xml_file, "Delete quota critical event with quota definition: " + sid)
									except:
										pass
									break

						# 37515	QUOTA EXHAUSTION EVENT
						if record_code == "375" and sub_record_code == "15" and update_type in ("1", "3"):
							quota_definition_sid	= self.getValue(oMessage, ".//oub:quota.definition.sid")
							exhaustion_date			= self.getDateValue(oMessage, ".//oub:exhaustion.date")

							# Action - Delete an critical event if it takes place after the critical date
							if exhaustion_date > self.critical_date:
								self.d("Delete quota exhaustion event with quota definition " + quota_definition_sid)
								oTransaction.remove (oMessage)
								self.register_update("375", "15", "delete", update_type_string, quota_definition_sid, xml_file, "Delete quota exhaustion event " + update_type_string + " instruction")

							# Action - search through this file's quota definitions and look for any items that have been deleted
							# If the quota definition has been deleted, then delete the suspension period too
							for sid in quota_order_definition_list:
								if (quota_definition_sid == sid):
									try:
										oTransaction.remove (oMessage)
										self.register_update("375", "15", "delete", update_type_string, quota_definition_sid, xml_file, "Delete quota exhaustion event with quota definition: " + sid)
									except:
										pass
									break

						# 37520	QUOTA REOPENING EVENT
						if record_code == "375" and sub_record_code == "20" and update_type in ("1", "3"):
							quota_definition_sid	= self.getValue(oMessage, ".//oub:quota.definition.sid")
							reopening_date			= self.getDateValue(oMessage, ".//oub:reopening.date")

							# Action - Delete an reopening event if it takes place after the critical date
							if reopening_date > self.critical_date:
								oTransaction.remove (oMessage)
								self.register_update("375", "20", "delete", update_type_string, quota_definition_sid, xml_file, "Delete quota reopening event with quota definition " + quota_definition_sid)

							# Action - search through this file's quota definitions and look for any items that have been deleted
							# If the quota definition has been deleted, then delete the reopening event too
							for sid in quota_order_definition_list:
								if (quota_definition_sid == sid):
									try:
										oTransaction.remove (oMessage)
										self.register_update("375", "20", "delete", update_type_string, quota_definition_sid, xml_file, "Delete quota reopening event with quota definition: " + sid)
									except:
										pass
									break

						# 37525	QUOTA UNSUSPENSION EVENT
						if record_code == "375" and sub_record_code == "25" and update_type in ("1", "3"):
							quota_definition_sid	= self.getValue(oMessage, ".//oub:quota.definition.sid")
							unsuspension_date		= self.getDateValue(oMessage, ".//oub:unsuspension.date")

							# Action - Delete an unsuspension event if it takes place after the critical date
							if unsuspension_date > self.critical_date:
								oTransaction.remove (oMessage)
								self.register_update("375", "25", "delete", update_type_string, quota_definition_sid, xml_file, "Delete quota unsuspension event with quota definition " + quota_definition_sid)

							# Action - search through this file's quota definitions and look for any items that have been deleted
							# If the quota definition has been deleted, then delete the unsuspension event too
							for sid in quota_order_definition_list:
								if (quota_definition_sid == sid):
									try:
										oTransaction.remove (oMessage)
										self.register_update("375", "25", "delete", update_type_string, quota_definition_sid, xml_file, "Delete quota unsuspension event with quota definition: " + sid)
									except:
										pass
									break

					"""
					# 43005	MEASURE COMPONENT
					if record_code == "430" and sub_record_code == "05":
						if update_type in ("1", "3"):
							measure_sid	= self.getValue(oMessage, ".//oub:measure.sid")
							removed_node = False
							for sid in measure_list:
								if (measure_sid == sid):
									oTransaction.remove (oMessage)
									self.register_update("430", "05", "delete", update_type_string, sid, xml_file, "Delete measure component for deleted measure with sid " + sid)
									removed_node = True
									break
							if not(removed_node):
								for s in self.log_list:
									if s.record_code == "430" and s.sub_record_code == "05" and (s.update_type_string in ("insert", "update")):
										if s.sid == measure_sid:
											oTransaction.remove (oMessage)
											self.register_update("430", "05", "delete", update_type_string, measure_sid, xml_file, "Delete measure component for deleted measure with sid " + measure_sid)
											break

					# 43010	MEASURE CONDITION
					# Look for any measure conditions in the current file that have a measure_sid that matches
					# one that has been deleted from the file - if so, then delete this instuction
					if record_code == "430" and sub_record_code == "10" and update_type in ("1", "3"):
						measure_sid	= self.getValue(oMessage, ".//oub:measure.sid")
						removed_node = False
						for sid in measure_list:
							if (measure_sid == sid):
								oTransaction.remove (oMessage)
								measure_condition_sid = self.getValue(oMessage, ".//oub:measure.condition.sid")
								self.register_update("430", "10", "delete", update_type_string, sid, xml_file, "Delete measure condition for deleted measure with sid " + sid)
								measure_condition_list.append(measure_condition_sid)
								removed_node = True
								break

						# Look in the log for any matching measure conditions that map to this one
						# If found, then delete the measure condition
						if not(removed_node):
							for s in self.log_list:
								if s.record_code == "430" and s.sub_record_code == "10" and (s.update_type_string in ("insert", "update")):
									if s.sid == measure_sid:
										oTransaction.remove (oMessage)
										self.register_update("430", "10", "delete", update_type_string, measure_sid, xml_file, "Delete measure condition for deleted measure with sid " + measure_sid)
										break

					# 43015	MEASURE EXCLUDED GEOGRAPHICAL AREA
					# Look in the current file for any excluded geo areas that map to any of the measure sids that have been removed.
					# If found, then delete them from the XML file
					if record_code == "430" and sub_record_code == "15" and update_type in ("1", "3"):
						measure_sid	= self.getValue(oMessage, ".//oub:measure.sid")
						removed_node = False
						for sid in measure_list:
							if (measure_sid == sid):
								oTransaction.remove (oMessage)
								self.register_update("430", "15", "delete", update_type_string, sid, xml_file, "Delete geographical area exclusion for deleted measure with sid " + sid)
								removed_node = True
								break

						# Look in the log file for any measure sids that match this measure component:
						# If found, then delete them from the XML file
						if not(removed_node):
							for s in self.log_list:
								if s.record_code == "430" and s.sub_record_code == "15" and (s.update_type_string in ("insert", "update")):
									if s.sid == measure_sid:
										oTransaction.remove (oMessage)
										self.register_update("430", "15", "delete", update_type_string, measure_sid, xml_file, "Delete geographical area exclusion for deleted measure with sid " + measure_sid)
										break

					# 43020	FOOTNOTE ASSOCIATION (MEASURE)
					if record_code == "430" and sub_record_code == "20" and update_type in ("1", "3"):
						measure_sid	= self.getValue(oMessage, ".//oub:measure.sid")
						removed_node = False
						for sid in measure_list:
							if (measure_sid == sid):
								oTransaction.remove (oMessage)
								self.register_update("430", "20", "delete", update_type_string, sid, xml_file, "Delete footnote association (measure) for deleted measure with sid " + sid)
								removed_node = True
								break

						if not(removed_node):
							for s in self.log_list:
								if s.record_code == "430" and s.sub_record_code == "20" and (s.update_type_string in ("insert", "update")):
									if s.sid == measure_sid:
										oTransaction.remove (oMessage)
										self.register_update("430", "20", "delete", update_type_string, measure_sid, xml_file, "Delete footnote association (measure) for deleted measure with sid " + measure_sid)
										break
										
					# 43025	MEASURE PARTIAL TEMPORARY STOP
					if record_code == "430" and sub_record_code == "25" and update_type in ("1", "3"):
						measure_sid	= self.getValue(oMessage, ".//oub:measure.sid")
						removed_node = False
						for sid in measure_list:
							if (measure_sid == sid):
								oTransaction.remove (oMessage)
								self.register_update("430", "25", "delete", update_type_string, sid, xml_file, "Delete partial temporary stop for deleted measure with sid " + sid)
								removed_node = True
								break

						if not(removed_node):
							for s in self.log_list:
								if s.record_code == "430" and s.sub_record_code == "25" and (s.update_type_string in ("insert", "update")):
									if s.sid == measure_sid:
										oTransaction.remove (oMessage)
										self.register_update("430", "25", "delete", update_type_string, measure_sid, xml_file, "Delete partial temporary stop for deleted measure with sid " + measure_sid)
										break
					"""
			# The third pass through looks at measure condition components
			# This removes meaure condition components that are created as a result of the measure conditions that have already been 
			# removed in the 2nd pass.

			"""
			for oTransaction in root.findall('.//env:transaction', self.namespaces):
				for oMessage in oTransaction.findall('.//env:app.message', self.namespaces):
					record_code			= oMessage.find(".//oub:record.code", self.namespaces).text
					sub_record_code		= oMessage.find(".//oub:subrecord.code", self.namespaces).text
					update_type			= oMessage.find(".//oub:update.type", self.namespaces).text
					update_type_string	= action_list[int(update_type) - 1]
					
					# 43011	MEASURE CONDITION COMPONENT
					# Look in the current file for any measure condition records that have been deleted from the XML file
					# If found, the delete the measure condition component instruction as well
					if record_code == "430" and sub_record_code == "11" and update_type in ("1", "3"):
						measure_condition_sid = self.getNumberValue(oMessage, ".//oub:measure.condition.sid")
						#print (measure_condition_sid)
						removed_node = False

						for sid in measure_condition_list:
							if (int(measure_condition_sid) == int(sid)):
								#print ("Found a condition component to delete")
								#sys.exit()
								oTransaction.remove (oMessage)
								self.register_update("430", "11", "delete", update_type_string, str(sid), xml_file, "Delete measure condition component for deleted measure condition with sid " + str(measure_condition_sid))
								removed_node = True
								break

						# Then, look into the log and find any matching measure conditions, from which components
						# would also need to get removed. Then delete those instructions
						if not(removed_node):
							for s in self.log_list:
								if s.record_code == "430" and s.sub_record_code == "10" and (s.update_type_string in ("insert", "update")):
									if s.sid == measure_condition_sid:
										oTransaction.remove (oMessage)
										self.register_update("430", "11", "delete", update_type_string, measure_condition_sid, xml_file, "Delete measure condition component for deleted measure condition with sid " + measure_condition_sid)
										break

			"""
			# Loop through the transactions, looking for empty transactions, where the sub messages have all been deleted
			# If found, then delete them all
			self.d("Delete all empty transaction nodes")
			for oTransaction in root.findall('.//env:transaction', self.namespaces):
				count = 0
				for oMessage in oTransaction.findall('.//env:app.message', self.namespaces):
					count += 1
				if count == 0:
					root.remove (oTransaction)

		#print ("Measure count: ", measure_count)
		# Write the XML node tree out in full
		tree.write(open(self.TEMP_FILE, "wb"), encoding = "utf8")
		
		# Reopen the file and correct the XML errors
		f = open(self.TEMP_FILE, "r", encoding = "utf-8") 
		s = f.read()
		f.close()

		s = re.sub("'utf8'", r'"UTF-8"', s)
		s = re.sub("'1.0'", r'"1.0"', s)
		s = re.sub("><", ">\n            <", s)
		s = re.sub(r'xmlns:env=', r'xmlns=', s)
		s = re.sub(r'xmlns:oub=', r'xmlns:env=', s)
		s = re.sub(r':TARIC:MESSAGE:', r':TARIC:TEMPMESSAGE:', s)
		s = re.sub(r':GENERAL:ENVELOPE:', r':TARIC:MESSAGE:', s)
		s = re.sub(r':TARIC:TEMPMESSAGE:', r':GENERAL:ENVELOPE:', s)
		#s = re.sub("<oub:transmission>", r'<oub:transmission xmlns:oub="urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0" xmlns:env="urn:publicid:-:DGTAXUD:GENERAL:ENVELOPE:1.0">', s)
		s = re.sub("<oub:transmission>", r'<oub:transmission xmlns:env="urn:publicid:-:DGTAXUD:GENERAL:ENVELOPE:1.0" xmlns:oub="urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0">', s)
		
		# Write the regulation log file
		f = open(self.regulation_log_filename, "w", encoding="utf-8")
		my_set = set(self.regulation_list)
		self.regulation_log = ""
		
		self.regulation_log += "New regulations\n"
		if len(self.new_regulation_list) > 0:
			for r in self.new_regulation_list:
				self.regulation_log += r.regulation_id + "," + r.information_text + "\n"
		else:
			self.regulation_log += "No new regulations\n"
		
		self.regulation_log += "\nRegulations referenced\n"
		for r in my_set:
			my_desc = ""
			if len(self.new_regulation_list) > 0:
				for nr in self.new_regulation_list:
					if nr.regulation_id == r:
						my_desc = "<NEW> " + nr.reg_type + " : " + nr.information_text
						break
			self.regulation_log += r + "," + my_desc + "\n"

		f.write(self.regulation_log)
		f.close()

		# Write the XML file
		f = open(self.TEMP_FILE, "w", encoding="utf-8") 
		f.write(s)
		f.close()
		self.validate(temp=True)

		filenames = [self.TEMP_FILE]
		
		if sMerge1 not in ("-p", "p", "profile", "-profile"):
			if sMerge1 != "":
				filenames.append (os.path.join(self.MERGE_DIR, sMerge1))
			if sMerge2 != "":
				filenames.append (os.path.join(self.MERGE_DIR, sMerge2))
			if sMerge3 != "":
				filenames.append (os.path.join(self.MERGE_DIR, sMerge3))
			if sMerge4 != "":
				filenames.append (os.path.join(self.MERGE_DIR, sMerge4))
			if sMerge5 != "":
				filenames.append (os.path.join(self.MERGE_DIR, sMerge5))
			if sMerge6 != "":
				filenames.append (os.path.join(self.MERGE_DIR, sMerge6))
			if sMerge7 != "":
				filenames.append (os.path.join(self.MERGE_DIR, sMerge7))
			if sMerge8 != "":
				filenames.append (os.path.join(self.MERGE_DIR, sMerge8))
			if sMerge9 != "":
				filenames.append (os.path.join(self.MERGE_DIR, sMerge9))
			if sMerge10 != "":
				filenames.append (os.path.join(self.MERGE_DIR, sMerge10))
		else:
			if sMerge2 == "":
				sys.exit()
			else:
				import_profile = sMerge2
				if ".txt" not in import_profile:
					import_profile += ".txt"
				import_file = os.path.join(self.IMPORT_PROFILE_DIR, import_profile)
				#print (import_file)
				with open(import_file) as csv_file:
					csv_reader = csv.reader(csv_file, delimiter = ",")
					for row in csv_reader:
						filenames.append (os.path.join(self.MERGE_DIR, row[0]))

		
		iCount = len(filenames)
		if iCount > 1:
			self.d("Merging in additional files", True)
		iLoop = 0
		with open(self.xml_file_Out, 'w') as outfile:
			for fname in filenames:
				print ("   - " + fname)
				iLoop += 1
				with open(fname) as infile:
					for line in infile:
						
						# Is the first file and not the last file: lose the tail only
						if iLoop == 1 and iLoop != iCount:
							if not("</env:envelope" in line):
								outfile.write(line)

						# Is the first file and is also the last file: copy the entire file
						if iLoop == 1 and iLoop == iCount:
							outfile.write(line)

						# Not the first file and not the last file: lose the top and tail
						if iLoop != 1 and iLoop != iCount:
							if not("<?xml" in line) and not("env:envelope" in line):
								outfile.write(line)

						# Not the first file and is the last file: lose the top only
						if iLoop != 1 and iLoop == iCount:
							if not("<?xml" in line) and not("<env:envelope" in line):
								outfile.write(line)

		self.validate()


	def validate(self, temp=False):
		if temp:
			s = self.TEMP_FILE
			msg = "Validating the initial XML file against the Taric 3 schema"
		else:
			s = self.xml_file_Out
			msg = "Validating the final XML file against the Taric 3 schema"
		
		self.d(msg)
		schema_path = os.path.join(self.SCHEMA_DIR, "envelope.xsd")
		my_schema = xmlschema.XMLSchema(schema_path)
		try:
			if my_schema.is_valid(s):
				self.d("The file validated successfully")
			else:
				self.d("The file did not validate")
		except:
			self.d("The file did not validate and crashed the validator")

	def validateMetadata(self):
		self.d("Validating the metadata XML file against the metadata schema")
		schema_path = os.path.join(self.SCHEMA_DIR, "BatchFileInterfaceMetadata-1.0.7.xsd")
		my_schema = xmlschema.XMLSchema(schema_path)
		try:
			if my_schema.is_valid(self.metadata_filepath):
				self.d("The metadata file validated successfully.")
			else:
				self.d("The metadata file did not validate.")
		except:
			self.d("The metadata file did not validate and crashed the validator.")

	def getValue(self, node, xpath, return_null = False):
		try:
			s = node.find(xpath, self.namespaces).text
		except:
			if return_null:
				s = None
			else:
				s = ""
		return (s)

	def getNumberValue(self, node, xpath, return_null = False):
		try:
			s = int(node.find(xpath, self.namespaces).text)
		except:
			if return_null:
				s = None
			else:
				s = ""
		return (s)

	def getNode(self, node, xpath):
		try:
			s = node.find(xpath, self.namespaces)
		except:
			s = None
		return (s)

	def getDateValue(self, node, xpath, return_null = False):
		try:
			s = node.find(xpath, self.namespaces).text
			s = datetime.strptime(s, "%Y-%m-%d")
		except:
			if return_null:
				s = None
			else:
				s = ""
		return (s)
	
	def getIndex(self, node, xpath):
		index = -1
		for child in node.iter():
			#print (child.tag)
			index += 1
			s = child.tag.replace("{urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0}", "")
			if s == xpath:
				break
		return index

	def add_edit_node(self, oElement, new_node, after, new_node_text):
		after = after.replace("oub:", "")
		s = self.getValue(oElement, new_node)
		if s == "":
			index = self.getIndex(oElement, after)
			new_element      = ET.Element(new_node)
			new_element.text = new_node_text
			oElement.insert(index, new_element)
		else:
			node = self.getNode(oElement, new_node)
			node.text = new_node_text


	def setNode(self, oElement, xpath, new_node_text):
		node = self.getNode(oElement, xpath)
		node.text = new_node_text

	def d(self, s, include_indent = True):
		if self.debug:
			if include_indent:
				s = "- " + s
			else:
				s = "\n" + s.upper()
			#print (s + "\n")
			print (s)

	def register_update(self, record_code, sub_record_code, python_action_string, update_type_string, sid, filename, desc):
		self.d(desc)

		# Write a record to the log file if the identical string does not already exist
		s = record_code + "," + sub_record_code + "," + update_type_string + "," + sid + "," + filename + "," + desc
		if not(s in self.log_list_string):
			f = open(self.LOG_FILE, "a")
			f.write(s + "\n")
			f.close()

		# Wherever there are deletions of future records, also add these to their own unique log
		if python_action_string == "delete":
			# First for measures
			if record_code == "430" and sub_record_code == "00":
				with open (self.LOG_FILE_MEASURE, "r") as myfile:
					LOG_FILE_MEASURE_content = myfile.read()
				if sid not in LOG_FILE_MEASURE_content:
					f = open(self.LOG_FILE_MEASURE, "a")
					f.write(sid + "\n")
					f.close()

			elif record_code == "430" and sub_record_code == "10":
			# And then for measure conditions
				with open (self.LOG_FILE_MEASURE_CONDITION, "r") as myfile:
					LOG_FILE_MEASURE_CONDITION_content = myfile.read()
				if sid not in LOG_FILE_MEASURE_CONDITION_content:
					f = open(self.LOG_FILE_MEASURE_CONDITION, "a")
					f.write(sid + "\n")
					f.close()


	def generateMetadata(self):
		self.d("Generating metadata file", False)
		# Get the handle
		filename = os.path.join(self.TEMPLATE_DIR, "metadata_template.xml")
		handle = open(filename, "r")
		self.metadata_XML = handle.read()

		self.correlation_id		= str(uuid.uuid1())
		self.checksum			= self.md5Checksum(self.xml_file_Out)
		self.filesize			= str(os.path.getsize(self.xml_file_Out))
		self.source_file_name	= self.output_filename

		self.metadata_XML = self.metadata_XML.replace("{CORRELATION_ID}",	self.correlation_id)
		self.metadata_XML = self.metadata_XML.replace("{CHECKSUM}", 		self.checksum)
		self.metadata_XML = self.metadata_XML.replace("{FILESIZE}", 		self.filesize)
		self.metadata_XML = self.metadata_XML.replace("{SOURCE_FILE_NAME}", self.source_file_name)

		# Write the output file
		self.metadata_filepath	= os.path.join(self.XML_OUT_DIR, self.metadata_filename)
		f = open(self.metadata_filepath, "w")
		f.write(self.metadata_XML)
		f.close()
		self.validateMetadata()

	def getTimestamp(self):
		ts = datetime.now()
		ts_string = datetime.strftime(ts, "%Y%m%dT%H%M%S")
		return (ts_string)

	def getDatestamp(self):
		ts = datetime.now()
		ts_string = datetime.strftime(ts, "%Y-%m-%d")
		return (ts_string)

	def convertFilename(self, s):
		if self.simple_filenames:
			if len(s) > 12:
				sequence_id		= s[14:16] + "0" + s[16:19]
				s = "DIT" + sequence_id + ".xml"
			else:
				sequence_id		= s[3:5] + "0" + s[5:8]
				s = "DIT" + sequence_id + ".xml"
		else:
			underscore_pos	= s.find('_')
			sequence_id	= s[14:19]
			if underscore_pos > -1:
				dt = s[0:underscore_pos].replace("-", "")
				ts = self.getTimestamp()
				s = "DIT_" + dt + "-" + dt + "-" + ts + "-" + sequence_id + ".XML"
			else:
				self.d("Fail")
				sys.exit()

		self.output_filename	= s
		self.metadata_filename	= s.replace(".", "_metadata.")
		#print (self.output_filename)
		#print (self.metadata_filename)

	def backup_database(self):
		DB_USER = 'postgres'
		DB_NAME = 'trade_tariff_181212b'
		ts = self.getTimestamp()
		filename = DB_NAME + "_" + ts + ".backup"

		destination = r'%s/%s' % (self.DUMP_DIR, filename)

		print ('Backing up %s database to %s' % (DB_NAME, destination))
		ps = subprocess.Popen(['pg_dump', '-U', DB_USER, '-f', destination, '-Fc', DB_NAME], stdout=subprocess.PIPE)
		output = ps.communicate()[0]
		for line in output.splitlines():
			print (line)


	def md5Checksum(self, filePath):
		with open(filePath, 'rb') as fh:
			m = hashlib.md5()
			while True:
				data = fh.read(8192)
				if not data:
					break
				m.update(data)
			return m.hexdigest()

	def clear(self): 
		# for windows 
		if name == 'nt': 
			_ = system('cls') 
		# for mac and linux(here, os.name is 'posix') 
		else: 
			_ = system('clear')

	def connect(self):
		self.conn = psycopg2.connect("dbname=" + self.DBASE + " user=postgres password" + self.p)

	def doprint(self, s):
		self.log_handle.write ("Message " + str(self.message_count) + " - " + s + "\n")
		print (s)

	def log_error(self, object, action, sid_key, id_key, transaction_id, message_id):
		self.conn.rollback()
		s = "Error - " + object + " " + action + " " + str(sid_key) + " " + str(id_key) + " " + str(transaction_id) + " " + str(message_id)
		print (s)
		self.log_handle.write (s + "\n")

	def import_xml(self, xml_file, prompt = True):
		self.convertFilename(xml_file)
		self.d("Importing file " + xml_file + " using database " + self.DBASE, False)

		if prompt:
			ret = self.yes_or_no("Do you want to continue?")
			if not (ret):
				sys.exit()

		# Check that this file has not already been imported
		sql = "SELECT import_file FROM ml.import_files WHERE import_file = '" + xml_file + "'"
		cur = self.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if len(rows) > 0:
			print ("\nFile", xml_file, "has already been imported - Aborting now\n")
			return

		self.xml_file_In		= os.path.join(self.IMPORT_DIR,  	xml_file)
		self.IMPORT_LOG_FILE	= os.path.join(self.IMPORT_LOG_DIR, "log_" + xml_file)
		self.IMPORT_LOG_FILE	= self.IMPORT_LOG_FILE.replace("xml", "txt")

		self.log_handle = open(self.IMPORT_LOG_FILE,"w") 
 
		# Load file
		ET.register_namespace('oub', 'urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0')
		ET.register_namespace('env', 'urn:publicid:-:DGTAXUD:GENERAL:ENVELOPE:1.0')
		tree = ET.parse(self.xml_file_In)
		root = tree.getroot()

		action_list = ["update", "delete", "insert"]

		self.message_count = 0

		for oTransaction in root.findall('.//env:transaction', self.namespaces):
			for oMessage in oTransaction.findall('.//env:app.message', self.namespaces):
				record_code			= oMessage.find(".//oub:record.code", self.namespaces).text
				sub_record_code		= oMessage.find(".//oub:subrecord.code", self.namespaces).text
				update_type			= oMessage.find(".//oub:update.type", self.namespaces).text
				transaction_id		= oMessage.find(".//oub:transaction.id", self.namespaces).text
				message_id			= oMessage.attrib["id"] # message id dummy"

				# 10000	FOOTNOTE TYPE
				if record_code == "100" and sub_record_code == "00":
					o = profile_10000_footnote_type()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 10000	FOOTNOTE TYPE DESCRIPTION
				if record_code == "100" and sub_record_code == "05":
					o = profile_10005_footnote_type_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 11000	CERTIFICATE TYPE
				if record_code == "110" and sub_record_code == "00":
					o = profile_11000_certificate_type()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 11005	CERTIFICATE TYPE DESCRIPTION
				if record_code == "110" and sub_record_code == "05":
					o = profile_11005_certificate_type_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 12000	ADDITIONAL CODE TYPE
				if record_code == "120" and sub_record_code == "00":
					o = profile_12000_additional_code_type()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 12005	ADDITIONAL CODE TYPE DESCRIPTION
				if record_code == "120" and sub_record_code == "05":
					o = profile_12005_additional_code_type_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 14000	MEASURE TYPE SERIES
				if record_code == "140" and sub_record_code == "00":
					o = profile_14000_measure_type_series()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 14005	MEASURE TYPE SERIES DESCRIPTION
				if record_code == "140" and sub_record_code == "05":
					o = profile_14005_measure_type_series_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 15000	REGULATION GROUP
				if record_code == "150" and sub_record_code == "00":
					o = profile_15000_regulation_group()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 15005	REGULATION GROUP DESCRIPTION
				if record_code == "150" and sub_record_code == "05":
					o = profile_15005_regulation_group_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 16000	REGULATION ROLE TYPE
				if record_code == "160" and sub_record_code == "00":
					o = profile_16000_regulation_role_type()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 16005	REGULATION ROLE TYPE DESCRIPTION
				if record_code == "160" and sub_record_code == "05":
					o = profile_16005_regulation_role_type_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 17000	PUBLICATION SIGLE
				if record_code == "170" and sub_record_code == "00":
					o = profile_17000_publication_sigle()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 20000	FOOTNOTE
				if record_code == "200" and sub_record_code == "00":
					o = profile_20000_footnote()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 20005	FOOTNOTE DESCRIPTION PERIOD
				if record_code == "200" and sub_record_code == "05":
					o = profile_20005_footnote_description_period()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 20010	FOOTNOTE DESCRIPTION
				if record_code == "200" and sub_record_code == "10":
					o = profile_20010_footnote_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 20500	CERTIFICATE
				if record_code == "205" and sub_record_code == "00":
					o = profile_20500_certificate()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 20505	CERTIFICATE DESCRIPTION PERIOD
				if record_code == "205" and sub_record_code == "05":
					o = profile_20505_certificate_description_period()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 20510	CERTIFICATE DESCRIPTION
				if record_code == "205" and sub_record_code == "10":
					o = profile_20510_certificate_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 21000	MEASUREMENT UNIT
				if record_code == "210" and sub_record_code == "00":
					o = profile_21000_measurement_unit()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 21005	MEASUREMENT UNIT DESCRIPTION
				if record_code == "210" and sub_record_code == "10":
					o = profile_21005_measurement_unit_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 21500	MEASUREMENT UNIT QUALIFIER
				if record_code == "215" and sub_record_code == "00":
					o = profile_21500_measurement_unit_qualifier()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 21505	MEASUREMENT UNIT QUALIFIER DESCRIPTION
				if record_code == "215" and sub_record_code == "05":
					o = profile_21505_measurement_unit_qualifier_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 22000	MEASUREMENT
				if record_code == "220" and sub_record_code == "00":
					o = profile_22000_measurement()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 23500	MEASURE TYPE
				if record_code == "235" and sub_record_code == "00":
					o = profile_23500_measure_type()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 23505	MEASURE TYPE DESCRIPTION
				if record_code == "235" and sub_record_code == "05":
					o = profile_23505_measure_type_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 24000	ADDITIONAL CODE TYPE / MEASURE TYPE
				if record_code == "240" and sub_record_code == "00":
					o = profile_24000_additional_code_type_measure_type()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 24500	ADDITIONAL CODE
				if record_code == "245" and sub_record_code == "00":
					o = profile_24500_additional_code()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 24505	ADDITIONAL CODE DESCRIPTION PERIOD
				if record_code == "245" and sub_record_code == "05":
					o = profile_24505_additional_code_description_period()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 24510	ADDITIONAL CODE DESCRIPTION
				if record_code == "245" and sub_record_code == "10":
					o = profile_24510_additional_code_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 25000	GEOGRAPHICAL AREA
				if record_code == "250" and sub_record_code == "00":
					o = profile_25000_geographical_area()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 25005	GEOGRAPHICAL AREA DESCRIPTION PERIOD
				if record_code == "250" and sub_record_code == "05":
					o = profile_25005_geographical_area_description_period()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 25010	GEOGRAPHICAL AREA DESCRIPTION
				if record_code == "250" and sub_record_code == "10":
					o = profile_25010_geographical_area_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 25015	GEOGRAPHICAL AREA MEMBERSHIP
				if record_code == "250" and sub_record_code == "15":
					o = profile_25015_geographical_area_membership()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 27500	COMPLETE ABROGATION REGULATION
				if record_code == "275" and sub_record_code == "00":
					o = profile_27500_complete_abrogation_regulation()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 28000	EXPLICIT ABROGATION REGULATION
				if record_code == "280" and sub_record_code == "00":
					o = profile_28000_explicit_abrogation_regulation()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 28500	BASE REGULATION
				if record_code == "285" and sub_record_code == "00":
					o = profile_28500_base_regulation()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 29000	MODIFICATION REGULATION
				if record_code == "290" and sub_record_code == "00":
					o = profile_29000_modification_regulation()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 29500	PROROGATION REGULATION
				if record_code == "295" and sub_record_code == "00":
					o = profile_29500_prorogation_regulation()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 29505	PROROGATION REGULATION ACTION
				if record_code == "295" and sub_record_code == "05":
					o = profile_29505_prorogation_regulation_action()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 30000	FULL TEMPORARY STOP REGULATION
				if record_code == "300" and sub_record_code == "00":
					o = profile_30000_full_temporary_stop_regulation()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 30500	REGULATION REPLACEMENT
				if record_code == "305" and sub_record_code == "00":
					o = profile_30500_regulation_replacement()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 35000	MEASURE CONDITION
				if record_code == "350" and sub_record_code == "00":
					o = profile_35000_measure_condition_code()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 35005	MEASURE CONDITION DESCRIPTION
				if record_code == "350" and sub_record_code == "05":
					o = profile_35005_measure_condition_code_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 35500	MEASURE ACTION
				if record_code == "355" and sub_record_code == "00":
					o = profile_35500_measure_action()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 35505	MEASURE ACTION DESCRIPTION
				if record_code == "355" and sub_record_code == "05":
					o = profile_35505_measure_action_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 36000	QUOTA ORDER NUMBER
				if record_code == "360" and sub_record_code == "00":
					o = profile_36000_quota_order_number()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 36005	QUOTA ORDER NUMBER ORIGIN
				if record_code == "360" and sub_record_code == "10":
					o = profile_36010_quota_order_number_origin()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 36000	QUOTA ORDER NUMBER ORIGIN EXCLUSION
				if record_code == "360" and sub_record_code == "15":
					o = profile_36015_quota_order_number_origin_exclusion()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 37000	QUOTA DEFINITION
				if record_code == "370" and sub_record_code == "00":
					o = profile_37000_quota_definition()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 37005	QUOTA ASSOCIATION
				if record_code == "370" and sub_record_code == "05":
					o = profile_37005_quota_association()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 37010	QUOTA BLOCKING PERIOD
				if record_code == "370" and sub_record_code == "10":
					o = profile_37010_quota_blocking_period()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 37015	QUOTA SUSPENSION PERIOD
				if record_code == "370" and sub_record_code == "15":
					o = profile_37015_quota_suspension_period()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 40000	GOODS NOMENCLATURE
				if record_code == "400" and sub_record_code == "00":
					o = profile_40000_goods_nomenclature()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 40005	GOODS NOMENCLATURE INDENT
				if record_code == "400" and sub_record_code == "05":
					o = profile_40005_goods_nomenclature_indent()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 40010	GOODS NOMENCLATURE DESCRIPTION PERIOD
				if record_code == "400" and sub_record_code == "10":
					o = profile_40010_goods_nomenclature_description_period()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 40015	GOODS NOMENCLATURE DESCRIPTION
				if record_code == "400" and sub_record_code == "15":
					o = profile_40015_goods_nomenclature_description()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 40020	FOOTNOTE ASSOCIATION GOODS NOMENCLATURE
				if record_code == "400" and sub_record_code == "20":
					o = profile_40020_footnote_association_goods_nomenclature()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 40035	GOODS NOMENCLATURE ORIGIN
				if record_code == "400" and sub_record_code == "35":
					o = profile_40035_goods_nomenclature_origin()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 40040	GOODS NOMENCLATURE SUCCESSOR
				if record_code == "400" and sub_record_code == "40":
					o = profile_40040_goods_nomenclature_successor()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 43000	MEASURE
				if record_code == "430" and sub_record_code == "00":
					o = profile_43000_measure()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 43005	MEASURE COMPONENT
				if record_code == "430" and sub_record_code == "05":
					o = profile_43005_measure_component()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 43010	MEASURE CONDITION
				if record_code == "430" and sub_record_code == "10":
					o = profile_43010_measure_condition()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 43011	MEASURE CONDITION COMPONENT
				if record_code == "430" and sub_record_code == "11":
					o = profile_43011_measure_condition_component()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 43015	MEASURE EXCLUDED GEOGRAPHICAL AREA
				if record_code == "430" and sub_record_code == "15":
					o = profile_43015_measure_excluded_geographical_area()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 43020	FOOTNOTE ASSOCIATION - MEASURE 
				if record_code == "430" and sub_record_code == "20":
					o = profile_43020_footnote_association_measure()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 43025	MEASURE PARTIAL TEMPORARY STOP
				if record_code == "430" and sub_record_code == "25":
					o = profile_43025_measure_partial_temporary_stop()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 44000	MONETARY EXCHANGE PERIOD
				if record_code == "440" and sub_record_code == "00":
					o = profile_44000_monetary_exchange_period()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)

				# 44005	MONETARY EXCHANGE RATE
				if record_code == "440" and sub_record_code == "05":
					o = profile_44005_monetary_exchange_rate()
					o.import_xml(self, update_type, oMessage, transaction_id, message_id)
		
		self.log_handle.close()

		# Register the load
		cur = self.conn.cursor()
		cur.execute("INSERT INTO ml.import_files (import_file) VALUES  ('" + xml_file + "')")
		#cur.execute("INSERT INTO ml.import_files (import_file) VALUES  (%s)", (xml_file))
		self.conn.commit()

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

	def yes_or_no(self, question):
		reply = str(input(question+' (y/n): ')).lower().strip()
		if reply[0] == 'y':
			return True
		if reply[0] == 'n':
			return False
		else:
			return yes_or_no("Uhhhh... please enter ")