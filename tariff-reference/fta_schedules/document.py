from datetime import datetime
import re
import os
import os, csv
import sys
import codecs

import functions as f
import glob as g

#from application import application
from duty        import duty
from quota_order_number import quota_order_number
from quota_definition import quota_definition
from measure import measure
from commodity import commodity
from quota_commodity import quota_commodity
from quota_balance import quota_balance

#app = g.app

class document(object):
	def __init__(self):
		self.footnote_list				= []
		self.duty_list					= []
		self.balance_list				= []
		self.supplementary_unit_list	= []
		self.seasonal_records			= 0
		self.wide_duty					= False

		print ("Creating FTA document for " + g.app.country_name + "\n")

		self.document_xml = ""
		
	def get_duties(self, instrument_type):
		app = g.app
		###############################################################
		# Get the duties
		if instrument_type == "preferences":
			measure_type_list = "'142', '145'"
		else:
			measure_type_list = "'143', '146'"

		if app.country_profile == "switzerland":			
			sql = """SELECT m.goods_nomenclature_item_id, m.additional_code_type_id, m.additional_code_id,
			m.measure_type_id, mc.duty_expression_id, mc.duty_amount, mc.monetary_unit_code,
			mc.measurement_unit_code, mc.measurement_unit_qualifier_code, m.measure_sid, m.ordernumber,
			m.validity_start_date, m.validity_end_date, m.geographical_area_id
			FROM ml.v5_2019 m LEFT OUTER JOIN measure_components mc ON m.measure_sid = mc.measure_sid
			WHERE (m.measure_type_id IN (""" + measure_type_list + """)
			AND m.geographical_area_id IN (""" + g.app.geo_ids + """)
			AND (m.validity_end_date > '2019-03-29' OR m.validity_end_date IS NULL))
			OR m.measure_sid = 3231905
			ORDER BY m.goods_nomenclature_item_id, m.measure_type_id, m.measure_sid, mc.duty_expression_id"""
		else:
			sql = """SELECT m.goods_nomenclature_item_id, m.additional_code_type_id, m.additional_code_id,
			m.measure_type_id, mc.duty_expression_id, mc.duty_amount, mc.monetary_unit_code,
			mc.measurement_unit_code, mc.measurement_unit_qualifier_code, m.measure_sid, m.ordernumber,
			m.validity_start_date, m.validity_end_date, m.geographical_area_id
			FROM ml.v5_2019 m LEFT OUTER JOIN measure_components mc ON m.measure_sid = mc.measure_sid
			WHERE m.measure_type_id IN (""" + measure_type_list + """)
			AND m.geographical_area_id IN (""" + g.app.geo_ids + """)
			AND (m.validity_end_date > '2019-03-29' OR m.validity_end_date IS NULL)
			ORDER BY m.goods_nomenclature_item_id, m.measure_type_id, m.measure_sid, mc.duty_expression_id"""
		
		#print (sql)
		#sys.exit()
		
		cur = app.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()

		# Do a pass through the duties table and create a full duty expression
		self.duty_list = []
		for row in rows:
			commodity_code					= f.mstr(row[0])
			additional_code_type_id			= f.mstr(row[1])
			additional_code_id				= f.mstr(row[2])
			measure_type_id					= f.mstr(row[3])
			duty_expression_id				= f.mstr(row[4])
			duty_amount						= row[5]
			monetary_unit_code				= f.mstr(row[6])
			monetary_unit_code				= monetary_unit_code.replace("EUR", "€")
			measurement_unit_code			= f.mstr(row[7])
			measurement_unit_qualifier_code = f.mstr(row[8])
			measure_sid						= f.mstr(row[9])
			quota_order_number_id			= f.mstr(row[10])
			geographical_area_id			= f.mstr(row[13])

			oDuty = duty(commodity_code, additional_code_type_id, additional_code_id, measure_type_id, duty_expression_id, duty_amount, monetary_unit_code, measurement_unit_code, measurement_unit_qualifier_code, measure_sid, quota_order_number_id, geographical_area_id)
			self.duty_list.append(oDuty)
		

	def get_quota_order_numbers(self):
		app = g.app
		# Get unique order numbers
		sql = """SELECT DISTINCT ordernumber FROM ml.v5_2019 m WHERE m.measure_type_id IN ('143', '146')
		AND m.geographical_area_id IN (""" + g.app.geo_ids + """) ORDER BY 1"""
		cur = app.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if len(rows) == 0:
			self.has_quotas = False
			return
		else:
			self.has_quotas = True

		self.quota_order_number_list = []
		self.q = []
		quota_order_number_list_flattened = ""
		csv_text = ""
		for row in rows:
			quota_order_number_id = row[0]
			qon = quota_order_number(quota_order_number_id)
			self.quota_order_number_list.append(qon)
			self.q.append (quota_order_number_id)
			quota_order_number_list_flattened += "'" + quota_order_number_id + "',"
			csv_text += quota_order_number_id + "\n"
		
		quota_order_number_list_flattened = quota_order_number_list_flattened.strip()
		quota_order_number_list_flattened = quota_order_number_list_flattened.strip(",")

		# Get the partial temporary stops, so that we can omit the suspended measures
		"""
		if quota_order_number_list_flattened != "":
			g.app.getPartialTemporaryStops(quota_order_number_list_flattened)

		for qon in self.quota_order_number_list:
			for mpts in app.partial_temporary_stops:
				if mpts.quota_order_number_id == qon.quota_order_number_id:
					qon.suspended = True
		"""

		filename = os.path.join(app.CSV_DIR, app.country_profile + "_quotas.csv")
		file = codecs.open(filename, "w", "utf-8")
		file.write(csv_text)
		file.close() 


	def get_quota_measures(self):
		app = g.app
		# Get the measures - in order to get the commodity codes and the duties
		# Just get the commodities and add to an array
		sql = """
		SELECT DISTINCT measure_sid, goods_nomenclature_item_id, ordernumber, validity_start_date,
		validity_end_date, geographical_area_id FROM ml.v5_2019 m
		WHERE measure_type_id IN ('143', '146') AND geographical_area_id IN (""" + g.app.geo_ids + """)
		ORDER BY goods_nomenclature_item_id, measure_sid
		"""
		#print ("GQM", sql)
		#sys.exit()
		cur = app.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if len(rows) == 0:
			self.has_quotas = False
			return

		self.measure_list = []
		for row in rows:
			measure_sid					= row[0]
			goods_nomenclature_item_id	= row[1]
			quota_order_number_id		= row[2]
			validity_start_date			= row[3]
			validity_end_date			= row[4]
			geographical_area_id		= row[5]

			my_measure = measure(measure_sid, goods_nomenclature_item_id, quota_order_number_id, validity_start_date, validity_end_date, geographical_area_id)
			self.measure_list.append (my_measure)
		
		# Step 2 - Having loaded all of the measures from the database, cycle through the list of duties (components)
		# previously loaded and assign to the measures where appropriate
		temp_commodity_list = []
		for my_measure in self.measure_list:
			for d in self.duty_list:
				if (int(my_measure.measure_sid) == int(d.measure_sid)):
					my_measure.duty_list.append(d)
					my_measure.assigned = True
					temp_commodity_list.append(my_measure.commodity_code + "|" + my_measure.quota_order_number_id)

			my_measure.combine_duties()

		# Step 3 - Create commodity objects that relate all of the measures together
		temp_commodity_set = set(temp_commodity_list)
		quota_commodity_list = []
		for item in temp_commodity_set:
			item_split				= item.split("|")
			code					= item_split[0]
			quota_order_number_id	= item_split[1]
			obj = quota_commodity(code, quota_order_number_id)
			quota_commodity_list.append(obj)

		quota_commodity_list.sort(key=lambda x: x.commodity_code, reverse = False)
		
		# Step 4 - Assign all relevant measures to the commodity code
		for my_commodity in quota_commodity_list:
			for my_measure in self.measure_list:
				if (my_measure.commodity_code == my_commodity.commodity_code) and (my_measure.quota_order_number_id == my_commodity.quota_order_number_id):
					#if my_measure.quota_order_number_id == "092115":
					#	print ("092115 found", my_measure.combined_duty)
					my_commodity.measure_list.append(my_measure)

		for my_commodity in quota_commodity_list:
			my_commodity.resolve_measures()

		for my_commodity in quota_commodity_list:
			for qon in self.quota_order_number_list:
				if my_commodity.quota_order_number_id == qon.quota_order_number_id:
					qon.commodity_list.append (my_commodity)
					break


	def get_quota_balances_from_csv(self):
		app = g.app
		if self.has_quotas == False:
			return
		with open(app.BALANCE_FILE, "r") as f:
			reader = csv.reader(f)
			temp = list(reader)
		for balance in temp:
			try:
				quota_order_number_id	= balance[0].strip()
				country					= balance[1]
				method					= balance[2]
				y1_balance				= balance[9]
				yx_balance				= balance[10]
				yx_start				= balance[11]
				measurement_unit_code	= balance[12].strip()
				origin_quota			= balance[13].strip()
				addendum				= balance[14].strip()

				if measurement_unit_code == "KGM":
					measurement_unit_code = "KGM"

				if quota_order_number_id not in ("", "Quota order number"):
					qb = quota_balance(quota_order_number_id, country, method, y1_balance, yx_balance, yx_start, measurement_unit_code, origin_quota, addendum)
				
					self.balance_list.append(qb)
			except:
				pass


	def get_quota_definitions(self):
		app = g.app
		if self.has_quotas == False:
			return

		# Now get the quota definitions - this just gets quota definitions for FCFS quota
		# Any licensed quotas with first three characters "094" needs there to be an additional step to get the balances
		# from a CSV file - as per function "get_quota_balances_from_csv" above

		my_order_numbers = f.list_to_sql(self.q)
		sql = """SELECT * FROM quota_definitions WHERE quota_order_number_id IN (""" + my_order_numbers + """)
		AND validity_start_date >= '2018-01-01' ORDER BY quota_order_number_id"""
		cur = app.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		self.quota_definition_list = []
		for row in rows:
			quota_definition_sid			= row[0]
			quota_order_number_id			= row[1]
			validity_start_date				= row[2]
			validity_end_date				= row[3]
			quota_order_number_sid			= row[4]
			volume							= row[5]
			initial_volume					= row[6]
			measurement_unit_code			= row[7]
			maximum_precision				= row[8]
			critical_state					= row[9]
			critical_threshold				= row[9]
			monetary_unit_code				= row[10]
			measurement_unit_qualifier_code	= row[11]

			qd = quota_definition(quota_definition_sid, quota_order_number_id, validity_start_date, validity_end_date,
			quota_order_number_sid, volume, initial_volume, measurement_unit_code, maximum_precision, critical_state,
			critical_threshold, monetary_unit_code, measurement_unit_qualifier_code)
			
			if len(self.balance_list) > 0:
				for qb in self.balance_list:
					if qb.quota_order_number_id == qd.quota_order_number_id:
						qd.initial_volume = int(qb.y1_balance)
						qd.volume_yx	= int(qb.yx_balance)
						qd.addendum		= qb.addendum
						qd.format_volumes()
						break

			qd.format_volumes()
			self.quota_definition_list.append(qd)

		# This process goes through the balance list (derived from the CSV) and assigns both the 2020 balance to the
		# quota definition object, as well as assigning the 2019 and 2020 balance to the licensed quotas
		# Stop press: I need to also assign the 2019 balance from the CSV, as this is a process run entirely againt
		# the EU's files, not the UK's
		for qon in self.quota_order_number_list:
			if qon.quota_order_number_id[0:3] == "094":
				# For licensed quotas, we need to create a brand new (artifical, not DB-persisted) definition, for use in the
				# creation of the FTA document only
				if len(self.balance_list) > 0:
					for qb in self.balance_list:
						if qb.quota_order_number_id == qon.quota_order_number_id:
							if qb.measurement_unit_code == "":
								qb.measurement_unit_code = "KGM"
							d1 = datetime.strptime(qb.yx_start, "%d/%m/%Y")
							d2 = qb.yx_end
							qd = quota_definition(0, qon.quota_order_number_id, d1, d2, 0, int(qb.y1_balance), int(qb.y1_balance), qb.measurement_unit_code, 3, "Y", 90, "", "")
							qd.volume_yx = int(qb.yx_balance)
							qd.addendum = qb.addendum.strip()
							qd.format_volumes()
							self.quota_definition_list.append(qd)
							break

		# Finally, add the quota definitions, replete with their new balances
		# to the relevant quota order numbers
		for qon in self.quota_order_number_list:
			for qd in self.quota_definition_list:
				if qd.quota_order_number_id == qon.quota_order_number_id:
					qon.quota_definition_list.append (qd)
					break

		# Now get the quota origins from the balance file
		for qon in self.quota_order_number_list:
			if len(self.balance_list) > 0:
				for qb in self.balance_list:
					if qb.quota_order_number_id == qon.quota_order_number_id:
						qon.origin_quota = qb.origin_quota
						break

		# Now get the 2019 start date from the balance file
		for qon in self.quota_order_number_list:
			if len(self.balance_list) > 0:
				for qb in self.balance_list:
					if qb.quota_order_number_id == qon.quota_order_number_id:
						qon.validity_start_date_2019 = qb.validity_start_date_2019
						qon.validity_end_date_2019 = qb.validity_end_date_2019
						break

	def print_quotas(self):
		app = g.app
		print (" - Getting quotas")
		if self.has_quotas == False:
			self.document_xml = self.document_xml.replace("{QUOTA TABLE GOES HERE}", "")
			return
		table_content = ""

		for qon in self.quota_order_number_list:
			# Check balance info has been provided, if not then do not display
			balance_found = False
			for bal in self.balance_list:
				if bal.quota_order_number_id == qon.quota_order_number_id:
					balance_found = True
					break

			#if not balance_found:
			#	print ("Quota balance not found", qon.quota_order_number_id)


			if balance_found:
				if len(qon.quota_definition_list) > 1:
					print ("More than one definition - we must be in Morocco")

				if len(qon.quota_definition_list) == 0:
					# if there are no definitions, then, either this is a screwed quota and the database is missing definition
					# entries, or this is a licensed quota, that we have somehow missed beforehand? Check get_quota_definitions
					# which should avoid this eventuality.
					qon.validity_start_date				= datetime.strptime("2019-03-29", "%Y-%m-%d")
					qon.validity_end_date               = datetime.strptime("2019-12-31", "%Y-%m-%d")
					print (qon.quota_order_number_id)
					qon.initial_volume                  = ""
					qon.volume_yx						= ""
					qon.measurement_unit_code           = ""
					qon.monetary_unit_code              = ""
					qon.measurement_unit_qualifier_code = ""
				else:
					qon.validity_start_date				= qon.quota_definition_list[0].validity_start_date
					qon.validity_end_date               = qon.quota_definition_list[0].validity_end_date
					qon.initial_volume                  = qon.quota_definition_list[0].formatted_initial_volume
					qon.volume_yx						= qon.quota_definition_list[0].formatted_volume_yx
					qon.addendum						= qon.quota_definition_list[0].addendum
					qon.measurement_unit_code           = qon.quota_definition_list[0].measurement_unit_code
					qon.monetary_unit_code              = qon.quota_definition_list[0].monetary_unit_code
					qon.measurement_unit_qualifier_code = qon.quota_definition_list[0].measurement_unit_qualifier_code

				last_order_number	= "00.0000"
				last_duty			= "-1"
				
				for comm in qon.commodity_list:
					# Run a check to ensure that there are no 10 digit codes being added to the extract
					# where the 8 digit code is also being displayed, and the duties are the same
					if comm.commodity_code[8:] != "00":
						my_duty = comm.duty_string
						for sub_commodity in qon.commodity_list:
							if sub_commodity.commodity_code == comm.commodity_code[0:8] + "00":
								if sub_commodity.duty_string == my_duty:
									comm.suppress = True


					comm.suppress = False
					if comm.suppress == False:
						insert_divider = False
						insert_duty_divider = False
						row_string = app.sQuotaTableRowXML
						row_string = row_string.replace("{COMMODITY_CODE}",   		comm.commodity_code_formatted)

						if (last_order_number == qon.quota_order_number_id):
							row_string = row_string.replace("{QUOTA_ORDER_NUMBER}",		"")
							row_string = row_string.replace("{ORIGIN_QUOTA}",   		"")
							row_string = row_string.replace("{QUOTA_VOLUME}",			"")
							row_string = row_string.replace("{QUOTA_OPEN_DATE}",		"")
							row_string = row_string.replace("{QUOTA_CLOSE_DATE}",		"")
							row_string = row_string.replace("{QUOTA_OPEN_DATE_2019}",	"")
							row_string = row_string.replace("{QUOTA_CLOSE_DATE_2019}",	"")
							row_string = row_string.replace("{2019_QUOTA_VOLUME}",		"")
							#row_string = row_string.replace("<!--OPT//--><w:r><w:br/></w:r><!--OPT//-->",		"")
							row_string = re.sub("<!-- Begin Quota Volume cell //-->.*<!-- End Quota Volume cell //-->", '<!-- Begin Quota Volume cell //-->\n<w:tc><w:tcPr><w:vMerge/></w:tcPr><w:p><w:pPr><w:pStyle w:val="NormalinTable"/></w:pPr><w:r><w:t></w:t></w:r></w:p></w:tc>\n<!-- End Quota Volume cell //-->', row_string, flags=re.DOTALL)
							
						else:
							if qon.suspended:
								row_string = row_string.replace("{QUOTA_ORDER_NUMBER}",		qon.quota_order_number_id_formatted + " (suspended)")
							else:
								row_string = row_string.replace("{QUOTA_ORDER_NUMBER}",		qon.quota_order_number_id_formatted)

							row_string = row_string.replace("{ORIGIN_QUOTA}",   		qon.origin_quota)
							if qon.addendum != "":
								row_string = row_string.replace("{QUOTA_VOLUME}",			qon.volume_yx + " + " + qon.addendum)
							else:
								row_string = row_string.replace("{QUOTA_VOLUME}",			qon.volume_yx)
							
							try:
								row_string = row_string.replace("{QUOTA_OPEN_DATE_2019}",	datetime.strftime(qon.validity_start_date_2019, '%d/%m/%Y'))
							except:
								print (qon.quota_order_number_id)
							row_string = row_string.replace("{QUOTA_CLOSE_DATE_2019}",	datetime.strftime(qon.validity_end_date_2019, '%d/%m/%Y'))
							row_string = row_string.replace("{QUOTA_OPEN_DATE}",		datetime.strftime(qon.validity_start_date, '%d/%m'))
							row_string = row_string.replace("{QUOTA_CLOSE_DATE}",		datetime.strftime(qon.validity_end_date, '%d/%m'))
							row_string = row_string.replace("{2019_QUOTA_VOLUME}",		str(qon.initial_volume).strip() + " (2019)")
							insert_divider = True

						#if qon.quota_order_number_id == "092115":
						#	print ("Duty string", comm.duty_string)
						
						if comm.duty_string != last_duty:
							row_string = row_string.replace("{PREFERENTIAL_DUTY_RATE}",	comm.duty_string)
							insert_duty_divider = True
						else:
							row_string = row_string.replace("{PREFERENTIAL_DUTY_RATE}",	"")

						if insert_divider == True:
							row_string = row_string.replace("<w:tc>", "<w:tc>\n" + app.sHorizLineXML)
						elif insert_duty_divider == True:
							#row_string = row_string.replace("<w:tc>", "<w:tc>\n" + app.sHorizLineSoftXML)
							pass

						if (last_order_number == qon.quota_order_number_id):
							# Test code - replace the Origin quota cell with a merged cell
							row_string = re.sub("<!-- Begin quota number cell //-->.*<!-- End quota number cell //-->", '<!-- Begin quota number cell //-->\n<w:tc><w:tcPr><w:vMerge/></w:tcPr><w:p><w:pPr><w:pStyle w:val="NormalinTable"/></w:pPr><w:r><w:t></w:t></w:r></w:p></w:tc>\n<!-- End quota number cell //-->', row_string, flags=re.DOTALL)
							row_string = re.sub("<!-- Begin origin quota cell //-->.*<!-- End origin quota cell //-->", '<!-- Begin origin quota cell //-->\n<w:tc><w:tcPr><w:vMerge/></w:tcPr><w:p><w:pPr><w:pStyle w:val="NormalinTable"/></w:pPr><w:r><w:t></w:t></w:r></w:p></w:tc>\n<!-- End origin quota cell //-->', row_string, flags=re.DOTALL)
							row_string = re.sub("<!-- Begin Preferential Quota Duty Rate cell //-->.*<!-- End Preferential Quota Duty Rate cell //-->", '<!-- Begin Preferential Quota Duty Rate cell //-->\n<w:tc><w:tcPr><w:vMerge/></w:tcPr><w:p><w:pPr><w:pStyle w:val="NormalinTable"/></w:pPr><w:r><w:t></w:t></w:r></w:p></w:tc>\n<!-- End Preferential Quota Duty Rate cell //-->', row_string, flags=re.DOTALL)
							row_string = re.sub("<!-- Begin Quota Volume cell //-->.*<!-- End Quota Volume cell //-->", '<!-- Begin Quota Volume cell //-->\n<w:tc><w:tcPr><w:vMerge/></w:tcPr><w:p><w:pPr><w:pStyle w:val="NormalinTable"/></w:pPr><w:r><w:t></w:t></w:r></w:p></w:tc>\n<!-- End Quota Volume cell //-->', row_string, flags=re.DOTALL)
							row_string = re.sub("<!-- Begin Quota Open Date cell //-->.*<!-- End Quota Open Date cell //-->", '<!-- Begin Quota Open Date cell //-->\n<w:tc><w:tcPr><w:vMerge/></w:tcPr><w:p><w:pPr><w:pStyle w:val="NormalinTable"/></w:pPr><w:r><w:t></w:t></w:r></w:p></w:tc>\n<!-- End Quota Open Date cell //-->', row_string, flags=re.DOTALL)
							row_string = re.sub("<!-- Begin Quota Close Date cell //-->.*<!-- End Quota Close Date cell //-->", '<!-- Begin Quota Close Date cell //-->\n<w:tc><w:tcPr><w:vMerge/></w:tcPr><w:p><w:pPr><w:pStyle w:val="NormalinTable"/></w:pPr><w:r><w:t></w:t></w:r></w:p></w:tc>\n<!-- End Quota Close Date cell //-->', row_string, flags=re.DOTALL)
							row_string = re.sub("<!-- Begin Quota Close Date cell //-->.*<!-- End Quota Close Date cell //-->", '<!-- Begin Quota Close Date cell //-->\n<w:tc><w:tcPr><w:vMerge/></w:tcPr><w:p><w:pPr><w:pStyle w:val="NormalinTable"/></w:pPr><w:r><w:t></w:t></w:r></w:p></w:tc>\n<!-- End Quota Close Date cell //-->', row_string, flags=re.DOTALL)
							pass

						last_order_number = qon.quota_order_number_id
						last_duty = comm.duty_string

						table_content += row_string

		###########################################################################
		## Write the main document
		###########################################################################

		quota_xml = ""
		sTableXML = app.sQuotaTableXML
		width_list = [9, 9, 14, 16, 16, 10, 10, 16]

		sTableXML = sTableXML.replace("{WIDTH_QUOTA_NUMBER}", 					str(width_list[0]))
		sTableXML = sTableXML.replace("{WIDTH_ORIGIN_QUOTA}",					str(width_list[1]))
		sTableXML = sTableXML.replace("{WIDTH_COMMODITY_CODE}",					str(width_list[2]))
		sTableXML = sTableXML.replace("{WIDTH_PREFERENTIAL_QUOTA_DUTY_RATE}",	str(width_list[3]))
		sTableXML = sTableXML.replace("{WIDTH_QUOTA_VOLUME}",					str(width_list[4]))
		sTableXML = sTableXML.replace("{WIDTH_QUOTA_OPEN_DATE}",				str(width_list[5]))
		sTableXML = sTableXML.replace("{WIDTH_QUOTA_CLOSE_DATE}",				str(width_list[6]))
		sTableXML = sTableXML.replace("{WIDTH_2019_QUOTA_VOLUME}",				str(width_list[7]))

		sTableXML = sTableXML.replace("{TABLEBODY}", table_content)

		quota_xml += sTableXML

		self.document_xml = self.document_xml.replace("{QUOTA TABLE GOES HERE}", quota_xml)

	def write(self):
		app = g.app
		###########################################################################
		## WRITE document.xml
		###########################################################################
		#BASE_DIR	= os.path.dirname(os.path.realpath(__file__))
		#MODEL_DIR	= os.path.join(BASE_DIR, "model")
		#WORD_DIR	= os.path.join(MODEL_DIR, "word")
		FILENAME	= os.path.join(app.WORD_DIR, "document.xml")

		file = codecs.open(FILENAME, "w", "utf-8")
		file.write(self.document_xml)
		file.close() 

		###########################################################################
		## Finally, ZIP everything up
		###########################################################################
		self.FILENAME = app.country_profile + "_annex.docx"
		self.word_filename = os.path.join(app.OUTPUT_DIR, self.FILENAME)
		f.zipdir(self.word_filename)

	def print_tariffs(self):
		app = g.app
		print (" - Getting preferential duties")

		# Step 1 - Call the database to get a list of preferential tariff measures that relate to the country in question
		# Switzerland must include a single  Liechtenstein measure as well
		if app.country_profile == "switzerland":
			sql = """SELECT DISTINCT measure_sid, goods_nomenclature_item_id, validity_start_date, validity_end_date,
			geographical_area_id FROM ml.v5_2019 m
			WHERE (m.geographical_area_id IN (""" + g.app.geo_ids + """) AND m.measure_type_id IN ('142', '145'))
			OR measure_sid = 3231905
			ORDER BY goods_nomenclature_item_id, validity_start_date ASC"""
		else:
			sql = """SELECT DISTINCT measure_sid, goods_nomenclature_item_id, validity_start_date, validity_end_date,
			geographical_area_id FROM ml.v5_2019 m
			WHERE m.geographical_area_id IN (""" + g.app.geo_ids + """) AND m.measure_type_id IN ('142', '145')
			ORDER BY goods_nomenclature_item_id, validity_start_date ASC"""

		cur = app.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		measure_list = []
		for row in rows:
			measure_sid				= row[0]
			commodity_code			= row[1]
			validity_start_date		= row[2]
			validity_end_date		= row[3]
			geographical_area_id	= row[4]

			my_measure = measure(measure_sid, commodity_code, "", validity_start_date, validity_end_date, geographical_area_id)
			measure_list.append (my_measure)


		# Step 2 - Having loaded all of the measures from the database, cycle through the list of duties (components) previously
		# loaded, assign to the measures where appropriate
		temp_commodity_list = []
		for my_measure in measure_list:
			for d in self.duty_list:
				if int(my_measure.measure_sid) == int(d.measure_sid):
					my_measure.duty_list.append(d)
					my_measure.assigned = True
					temp_commodity_list.append(my_measure.commodity_code)

			# Create a single string that completely defines the measure's duties
			my_measure.combine_duties()

		# Step 3 - Create a list of unique commodity objects that relate all of the measures together
		temp_commodity_set = set(temp_commodity_list)
		commodity_list = []
		for code in temp_commodity_set:
			obj = commodity(code)
			commodity_list.append(obj)
		commodity_list.sort(key=lambda x: x.commodity_code, reverse = False)

		# Step 4 - Assign all relevant measures to the commodity code
		for my_commodity in commodity_list:
			for my_measure in measure_list:
				if my_measure.commodity_code == my_commodity.commodity_code:
					my_commodity.measure_list.append(my_measure)

		for my_commodity in commodity_list:
			my_commodity.resolve_measures()

		# Run a check to ensure that there are no 10 digit codes being added to the extract
		# where the 8 digit code is also being displayed, and the duties are the same
		for my_measure in measure_list:
			if my_measure.commodity_code[8:] != "00":
				my_duty = my_measure.combined_duty
				for sub_commodity in measure_list:
					if sub_commodity.commodity_code == my_measure.commodity_code[0:8] + "00":
						if sub_commodity.combined_duty == my_duty:
							my_measure.suppress_row = True


		###########################################################################
		## Output the rows to buffer
		###########################################################################

		table_content = ""
		for my_commodity in commodity_list:
			row_string = app.sTableRowXML
			row_string = row_string.replace("{COMMODITY}",   my_commodity.commodity_code_formatted)
			s = my_commodity.duty_string
			if s.endswith("<w:r><w:br/></w:r>"):
				s = s[:-18]
			row_string = row_string.replace("{DUTY}",        f.surround(s))

			table_content += row_string

		###########################################################################
		## Write the main document
		###########################################################################

		tariff_xml = ""

		sTableXML = app.sTableXML
		width_list = [400, 1450, 1150, 2000]
		sTableXML = sTableXML.replace("{WIDTH_CLASSIFICATION}", str(width_list[0]))
		sTableXML = sTableXML.replace("{WIDTH_DUTY}",			str(width_list[1]))

		sTableXML = sTableXML.replace("{TABLEBODY}", table_content)

		tariff_xml += sTableXML
		self.document_xml = app.sDocumentXML
		self.document_xml = self.document_xml.replace("{TARIFF TABLE GOES HERE}", tariff_xml)
