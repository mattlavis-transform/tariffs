import functions as f
import re
import os
import sys
import codecs
from application import application
from duty        import duty
from commodity   import commodity
from hierarchy   import hierarchy
from docxcompose.composer import Composer
from docx import Document
from zipfile import ZipFile, ZIP_DEFLATED


app = f.app

class chapter(object):
	def __init__(self, iChapter):
		self.chapter_id = iChapter
		if self.chapter_id in (77, 98, 99):
			return
		self.chapter_string				= str(self.chapter_id).zfill(2)
		self.footnote_list				= []
		self.duty_list					= []
		self.supplementary_unit_list	= []
		self.seasonal_records			= 0
		self.contains_authorised_use	= False

		print ("Creating " + app.document_type + " for chapter " + self.chapter_string)

		self.get_chapter_basics()

		self.get_section_details()
		self.get_chapter_description()
		self.get_duties()



	def format_chapter(self):
		if self.chapter_id in (77, 98, 99):
			return
		###############################################################
		# Get the table of classifications
		# Relevant to just the schedule - reallyt? Are you sure about this???
		sql = """SELECT DISTINCT goods_nomenclature_item_id, producline_suffix,
		description, number_indents, leaf FROM ml.goods_nomenclature_export_brexit('""" + self.chapter_string + """%')
		ORDER BY 1, 2"""

		cur = app.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		commodity_list = []
		# Make a list of commodities
		for rw in rows:
			commodity_code    	= rw[0]
			productline_suffix	= f.mstr(rw[1])
			description       	= rw[2]
			number_indents    	= f.mnum(rw[3])
			leaf              	= f.mnum(rw[4])

			my_commodity = commodity(commodity_code, description, productline_suffix, number_indents, leaf)
			commodity_list.append (my_commodity)

		# Assign duties to those commodities as appropriate
		if app.document_type == "schedule":
			for my_commodity in commodity_list:
				for d in self.duty_list:
					if my_commodity.commodity_code == d.commodity_code:
						if my_commodity.product_line_suffix == "80":
							my_commodity.duty_list.append(d)
							my_commodity.assigned = True

				my_commodity.combine_duties()
				my_commodity.format_commodity_code()

		###########################################################################
		# Get exceptions
		###########################################################################
		if app.document_type == "schedule":
			for my_commodity in commodity_list:
				my_commodity.check_for_specials()
				my_commodity.check_for_authorised_use()
				if my_commodity.combined_duty == "AU":
					self.contains_authorised_use = True
				self.seasonal_records += my_commodity.check_for_seasonal()


		#######################################################################################
		# Inherit any duties that exist at higher levels in the hierarchy down to lower levels
		# Inherit duties from the 1st item you find above you in the
		# list that has an indent lower than mine and a value
		#######################################################################################

		if app.document_type == "schedule":
			commodity_count = len(commodity_list)
			max_indent = -1
			for loop1 in range(0, commodity_count):
				my_commodity = commodity_list[loop1]
				if my_commodity.indents > max_indent:
					max_indent = my_commodity.indents
				if (my_commodity.combined_duty == ""): 
					
					for loop2 in range(loop1, 0, -1):
						upper_commodity = commodity_list[loop2]
						if upper_commodity.combined_duty != "" and upper_commodity.indents < my_commodity.indents:
							my_commodity.combined_duty = upper_commodity.combined_duty
							my_commodity.notes_list = upper_commodity.notes_list
							break
						if upper_commodity.indents <= 1:
							break


		###########################################################################
		# Hypothesis - we need to start at the deepest tier and then move upwards in order to work out
		# what commodities are siblings of what and suppress all 
		###########################################################################

		if app.document_type == "schedule":
			for indent in range(max_indent, 2, -1):
				for loop1 in range(0, commodity_count):
					my_commodity = commodity_list[loop1]
					if my_commodity.indents == indent:
						if my_commodity.significant_digits == 10:
							for loop2 in range(loop1, 0, -1):
								upper_commodity = commodity_list[loop2]
								if upper_commodity.indents == my_commodity.indents - 1:
									if upper_commodity.combined_duty == my_commodity.combined_duty:
										if my_commodity.commodity_code == "1001912020":
											print (my_commodity.commodity_code, my_commodity.indents, my_commodity.significant_digits, upper_commodity.commodity_code, upper_commodity.indents, upper_commodity.significant_digits, )
										my_commodity.suppress_row = True
										break
								if upper_commodity.indents <= 1:
									break

		
		###########################################################################
		## Only suppress the duty if the item is not PLS of 80
		## This will change to be - only supppress if not a leaf
		###########################################################################
		if app.document_type == "schedule":
			for loop1 in range(0, commodity_count):
				my_commodity = commodity_list[loop1]
				if my_commodity.product_line_suffix != "80":
					my_commodity.suppress_duty = True
				else:
					my_commodity.suppress_duty = False


		###########################################################################
		## Output the rows to buffer
		###########################################################################
		table_content = ""
		for my_commodity in commodity_list:
			if my_commodity.suppress_row == False:
				if app.document_type == "schedule":
					my_commodity.check_for_mixture()
					my_commodity.combine_notes()
				row_string = app.sTableRowXML
				row_string = row_string.replace("{COMMODITY}",   	my_commodity.commodity_code_formatted)
				row_string = row_string.replace("{DESCRIPTION}",	my_commodity.description)
				row_string = row_string.replace("{INDENT}",      	my_commodity.indent_string)
				if my_commodity.suppress_duty == True:
					row_string = row_string.replace("{DUTY}",       f.surround(""))
					row_string = row_string.replace("{NOTES}",      "")
				else:
					row_string = row_string.replace("{DUTY}",       f.surround(my_commodity.combined_duty))
					row_string = row_string.replace("{NOTES}",      my_commodity.notes_string)
				table_content += row_string
			
			
		###########################################################################
		## Write the main document
		###########################################################################

		body_string = ""
		if app.document_type == "schedule":
			if self.new_section == True:
				sHeading1XML = app.sHeading1XML
				sHeading1XML = sHeading1XML.replace("{HEADINGa}", "Section " + self.section_numeral)
				sHeading1XML = sHeading1XML.replace("{HEADINGb}", self.section_title)
				body_string += sHeading1XML

			sHeading2XML = app.sHeading2XML
			sHeading2XML = sHeading2XML.replace("{CHAPTER}", "Chapter " + self.chapter_string)
			sHeading2XML = sHeading2XML.replace("{HEADING}", self.chapter_description)
			body_string += sHeading2XML

		
		table_xml_string = app.table_xml_string

		if self.contains_authorised_use == True:
			width_list = [600, 1050, 1000, 2350]
		else:
			width_list = [600, 1050, 600, 2750]

		table_xml_string = table_xml_string.replace("{WIDTH_CLASSIFICATION}", str(width_list[0]))
		table_xml_string = table_xml_string.replace("{WIDTH_DUTY}",			str(width_list[1]))
		table_xml_string = table_xml_string.replace("{WIDTH_NOTES}",			str(width_list[2]))
		table_xml_string = table_xml_string.replace("{WIDTH_DESCRIPTION}",	str(width_list[3]))

		table_xml_string = table_xml_string.replace("{TABLEBODY}", table_content)

		body_string += table_xml_string
		document_xml_string = app.document_xml_string
		document_xml_string = document_xml_string.replace("{BODY}", body_string)

		# Final replaces on the super and subscripts
		document_xml_string = document_xml_string.replace("{TITLE1}", self.document_title.upper())
		document_xml_string = re.sub("<w:t>(.*)m2</w:t>", "<w:t>\g<1>m</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"superscript\"/></w:rPr><w:t>2</w:t>", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("<w:t>(.*)m3</w:t>", "<w:t>\g<1>m</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"superscript\"/></w:rPr><w:t>3</w:t>", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("<w:t>(.*)K2O</w:t>", "<w:t>\g<1>K</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>2</w:t></w:r><w:r><w:t>O</w:t>", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("<w:t>(.*)H2O2</w:t>", "<w:t>\g<1>H</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>2</w:t></w:r><w:r><w:t>O</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>2</w:t>", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("<w:t>(.*)P2O5</w:t>", "<w:t>\g<1>P</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>2</w:t></w:r><w:r><w:t>O</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>5</w:t>", document_xml_string, flags=re.MULTILINE)
		
		# Subscripts
		document_xml_string = re.sub("@(.)", '</w:t></w:r><w:r><w:rPr><w:vertAlign w:val="subscript"/></w:rPr><w:t>\\1</w:t></w:r><w:r><w:t>', document_xml_string, flags=re.MULTILINE)

		# Missing commas
		document_xml_string = re.sub("([0-9]),([0-9])%", "\\1.\\2%", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]) kg", "\\1.\\2 kg", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]) Kg", "\\1.\\2 kg", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]) C", "\\1.\\2 C", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9])kg", "\\1.\\2kg", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) g", "\\1.\\2 g", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3})g", "\\1.\\2g", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) dl", "\\1.\\2 dl", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) m", "\\1.\\2 m", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3})m", "\\1.\\2m", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) decitex", "\\1.\\2 decitex", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) l", "\\1.\\2 l", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) kW", "\\1.\\2 kW", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) W", "\\1.\\2 W", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) V", "\\1.\\2 V", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) Ah", "\\1.\\2 Ah", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) bar", "\\1.\\2 bar", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) cm", "\\1.\\2 cm", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) Nm", "\\1.\\2 Nm", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) kV", "\\1.\\2 kV", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) kHz", "\\1.\\2 kHz", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) kV", "\\1.\\2 kV", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) MHz", "\\1.\\2 MHz", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) μm", "\\1.\\2 μm", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) Ohm", "\\1.\\2 Ohm", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) dB", "\\1.\\2 dB", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("([0-9]),([0-9]{1,3}) kvar", "\\1.\\2 kvar", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("±([0-9]),([0-9]{1,3})", "±\\1.\\2", document_xml_string, flags=re.MULTILINE)
		document_xml_string = re.sub("€ ([0-9]{1,3}),([0-9]{1,3})", "€ \\1.\\2", document_xml_string, flags=re.MULTILINE)


		filename = os.path.join(app.MODEL_DIR, "word")
		filename = os.path.join(filename, "document.xml")
		file = codecs.open(filename, "w", "utf-8")
		file.write(document_xml_string)
		file.close()

		###########################################################################
		## Finally, ZIP everything up
		###########################################################################

		f.zipdir(self.word_filename)
		if app.document_type == "classification":
			self.prepend_chapter_notes()


	def get_chapter_basics(self):
		filename = app.document_type + "_" + self.chapter_string + ".docx"
		self.word_filename = os.path.join(app.OUTPUT_DIR, filename)
		if (app.document_type == "classification"):
			self.document_title = "UK Goods Classification"
		else:
			self.document_title = "UK Goods Schedule"



	def get_chapter_description(self):
		###############################################################
		# Get the chapter description
		# Relevant to both the classification and the schedule
		sql = "SELECT description FROM ml.chapters WHERE chapter = '" + self.chapter_string + "'"
		cur = app.conn.cursor()
		cur.execute(sql)
		row = cur.fetchone()
		try:
			self.chapter_description = row[0]
			self.chapter_description = self.chapter_description.replace(" Of ", " of ")
			self.chapter_description = self.chapter_description.replace(" Or ", " or ")
		except:
			self.chapter_description = ""


	def get_section_details(self):
		###############################################################
		# Get the section header
		# Relevant to both the classification and the schedule
		sql = """SELECT s.numeral, s.title, cs.section_id
		FROM goods_nomenclatures gn, chapters_sections cs, sections s
		WHERE gn.goods_nomenclature_sid = cs.goods_nomenclature_sid
		AND s.id = cs.section_id
		AND gn.goods_nomenclature_item_id = '""" + self.chapter_string + """00000000'"""
		cur = app.conn.cursor()
		cur.execute(sql)
		row = cur.fetchone()
		try:
			self.section_numeral = row[0]
		except:
			self.section_numeral = ""
			print ("Chapter does not exist")
			return
		self.section_title = row[1]
		self.sSectionID    = row[2]

		self.new_section = False
		for r in app.section_chapter_list:
			if int(r[0]) == self.chapter_id:
				self.new_section = r[2]
				break


	def prepend_chapter_notes(self):
		chapter_notes_filename = "chapter" + self.chapter_string + ".docx"
		chapter_notes_file = os.path.join(app.CHAPTER_NOTES_DIR, chapter_notes_filename)
		master_document = Document(chapter_notes_file)
		composer = Composer(master_document)
		my_chapter_file = Document(self.word_filename)
		composer.append(my_chapter_file)
		composer.save(self.word_filename)


	def get_chapter_notes_from_document_xml(self):
		path = os.path.join(app.CHAPTER_NOTES_DIR, "chapter01.docx")
		document = ZipFile(path)
		self.chapter_notes_xml = str(document.read('word/document.xml'))
		self.chapter_notes_xml = self.remove_header_footer_xml(self.chapter_notes_xml)
		document.close()

	
	def remove_header_footer_xml(self, s):
		s2 = ""
		pos = s.find("<w:body")
		pos2 = s.find("<w:sectPr")
		if pos > 0 and pos2 > 0:
			s2 = s[pos + 8: pos2]

		return (s2)


	def get_duties(self):
		###############################################################
		# Get the duties

		# And this is what is new
		sql = """SELECT m.goods_nomenclature_item_id, m.additional_code_type_id, m.additional_code_id,
		m.measure_type_id, mc.duty_expression_id, mc.duty_amount, mc.monetary_unit_code,
		mc.measurement_unit_code, mc.measurement_unit_qualifier_code, m.measure_sid /*,
		m.validity_start_date, m.validity_end_date, m.geographical_area_id*/
		FROM measure_components mc, ml.v5 m
		WHERE mc.measure_sid = m.measure_sid
		AND LEFT(m.goods_nomenclature_item_id, 2) = '""" + self.chapter_string + """'
		AND m.measure_type_id IN ('103', '105')
		ORDER BY m.goods_nomenclature_item_id, m.measure_type_id, m.measure_sid, mc.duty_expression_id"""

		cur = app.conn.cursor()
		cur.execute(sql)
		rows_duties = cur.fetchall()

		# Do a pass through the duties table and create a full duty expression
		self.duty_list = []
		for row in rows_duties:
			#print ("Found a duty")
			
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
			

			oDuty = duty(commodity_code, additional_code_type_id, additional_code_id, measure_type_id, duty_expression_id, duty_amount, monetary_unit_code, measurement_unit_code, measurement_unit_qualifier_code, measure_sid)
			self.duty_list.append(oDuty)
