import functions as f
import re
import os
import sys
import codecs
import xlsxwriter

from application import application
from duty        import duty
from commodity   import commodity
from hierarchy   import hierarchy

app = f.app

class chapter(object):
	def __init__(self, iChapter):
		self.chapter_id = iChapter
		if self.chapter_id in (77, 98, 99):
			return
		self.chapter_string = str(self.chapter_id).zfill(2)
		self.footnote_list = []
		self.duty_list = []
		self.local_duty_list = []
		self.supplementary_unit_list = []
		self.seasonal_records = 0
		self.wide_duty = False
		self.commodity_list = []

		print ("Creating " + app.sDocumentType + " for chapter " + self.chapter_string)

		self.getChapterBasics()

		self.getSection()
		self.getChapterDescription()
		self.get_mfn_duties()
		self.get_local_duties()
		self.get_local_quotas()

		self.section_notes = ""
		self.chapter_notes = ""

	def formatChapter(self):
		if self.chapter_id in (77, 98, 99):
			return
		###############################################################
		# Get the table of classifications
		sql = """SELECT DISTINCT goods_nomenclature_item_id, producline_suffix,
		description, number_indents, leaf FROM ml.goods_nomenclature_export_brexit('""" + self.chapter_string + """%')
		ORDER BY 1, 2"""

		cur = app.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		self.commodity_list = []
		for rw in rows:
			commodity_code    = rw[0]
			productline_suffix = f.mstr(rw[1])
			description       = rw[2]
			number_indents    = f.mnum(rw[3])
			leaf              = f.mnum(rw[4])

			my_commodity = commodity(commodity_code, description, productline_suffix, number_indents, leaf)
			self.commodity_list.append (my_commodity)

		for my_commodity in self.commodity_list:
			#print ("here")
			# Start with the duties
			for d in self.duty_list:
				#print (my_commodity.commodity_code_formatted)
				if my_commodity.commodity_code == d.commodity_code:
					if my_commodity.product_line_suffix == "80":
						my_commodity.duty_list.append(d)
						my_commodity.assigned = True
			
			# And then do the local duties
			for d in self.local_duty_list:
				if my_commodity.commodity_code == d.commodity_code:
					if my_commodity.product_line_suffix == "80":
						my_commodity.local_duty_list.append(d)
						my_commodity.assigned_local = True

			# And then do quotas
			for q in self.quota_list:
				if my_commodity.commodity_code == q:
					if my_commodity.product_line_suffix == "80":
						my_commodity.has_quota = True
			
			my_commodity.combine_duties()
			my_commodity.combine_local_duties()

		###########################################################################
		## Get exceptions
		###########################################################################
		if app.sDocumentType == "schedule":
			for my_commodity in self.commodity_list:
				my_commodity.checkforSIV()
				my_commodity.checkforVessel()
				my_commodity.checkforCivilAir()
				my_commodity.checkforAirworthiness()
				my_commodity.checkforAircraft()
				my_commodity.checkforPharmaceuticals()
				#my_commodity.checkforITA()
				#my_commodity.checkforMixture()
				my_commodity.checkforSpecials()
				my_commodity.checkforAuthorisedUse()
				my_commodity.checkforGeneralRelief()
				self.seasonal_records += my_commodity.checkforSeasonal()

		#####################################################################
		## Inherit up
		#####################################################################
		commodity_count = len(self.commodity_list)

		### The new bit - Inherit duties from the 1st item you find above you in the
		### list that has an indent lower than mine and a value
		for loop1 in range(0, commodity_count):
			my_commodity = self.commodity_list[loop1]
			if my_commodity.product_line_suffix == "80":
				if (my_commodity.combined_duty == "") and (my_commodity.leaf == 1):
					for loop2 in range(loop1 - 1 , 0, -1):
						upper_commodity = self.commodity_list[loop2]
						if upper_commodity.combined_duty != "" and upper_commodity.indents < my_commodity.indents:
							my_commodity.combined_duty = upper_commodity.combined_duty
							my_commodity.notes_list = upper_commodity.notes_list
							break
						if upper_commodity.indents >= my_commodity.indents or upper_commodity.indents == 0:
							break

		### And do the same with local duties
		for loop1 in range(0, commodity_count):
			my_commodity = self.commodity_list[loop1]
			if my_commodity.product_line_suffix == "80":
				if (my_commodity.combined_local_duty == "") and (my_commodity.leaf == 1):
					for loop2 in range(loop1 - 1 , 0, -1):
						upper_commodity = self.commodity_list[loop2]
						if upper_commodity.combined_local_duty != "" and upper_commodity.indents < my_commodity.indents:
							my_commodity.combined_local_duty = upper_commodity.combined_local_duty
							break
						if upper_commodity.indents >= my_commodity.indents or upper_commodity.indents == 0:
							break
		
		### And finally, do the same with quotas
		for loop1 in range(0, commodity_count):
			my_commodity = self.commodity_list[loop1]
			if my_commodity.product_line_suffix == "80":
				if (my_commodity.has_quota == False) and (my_commodity.leaf == 1):
					for loop2 in range(loop1 - 1 , 0, -1):
						upper_commodity = self.commodity_list[loop2]
						if upper_commodity.has_quota == True and upper_commodity.indents < my_commodity.indents:
							my_commodity.has_quota = True
							break
						if upper_commodity.indents >= my_commodity.indents or upper_commodity.indents == 0:
							break

		self.get_applied_duties()


		###########################################################################
		## Check for row suppression - We should not be suppressing rows 
		###########################################################################
		for loop1 in range(0, commodity_count):
			my_commodity.suppress_row = False
		
		###########################################################################
		## Only suppress the duty if the item is not PLS of 80
		## This will change to be - only supppress if not a leaf
		###########################################################################
		for loop1 in range(0, commodity_count):
			my_commodity = self.commodity_list[loop1]
			if my_commodity.leaf != 1:
				my_commodity.suppress_row = True
				my_commodity.suppress_duty = True
			else:
				my_commodity.suppress_row = False
				my_commodity.suppress_duty = False

		###########################################################################
		## Output the rows to buffer
		###########################################################################
		table_content = ""
		for my_commodity in self.commodity_list:
			if my_commodity.suppress_row == False:
				my_commodity.checkforMixture()
				my_commodity.combine_notes()
				row_string = app.sTableRowXML
				row_string = row_string.replace("{COMMODITY}",   	my_commodity.commodity_code_formatted)
				row_string = row_string.replace("{DESCRIPTION}",	my_commodity.description)
				row_string = row_string.replace("{INDENT}",      	my_commodity.indent_string)
				if my_commodity.suppress_duty == True:
					row_string = row_string.replace("{DUTY}",       f.surround(""))
					row_string = row_string.replace("{NOTES}",      "")
				else:
					#print ("not suppress duty", my_commodity.commodity_code, my_commodity.combined_duty)
					row_string = row_string.replace("{DUTY}",       f.surround(my_commodity.combined_duty))
					row_string = row_string.replace("{NOTES}",      my_commodity.notes_string)
				table_content += row_string
			
				# Write to excel
				f.wkbk.current_row += 1
				f.wkbk.write('A', my_commodity.commodity_code, f.wkbk.nowrap)
				#f.wkbk.write('B', my_commodity.description_excel, f.wkbk.indent_formats[my_commodity.indents])
				f.wkbk.write('B', my_commodity.description_excel, f.wkbk.wrap)
				if my_commodity.suppress_duty == False:
					f.wkbk.write('C', my_commodity.combined_duty, f.wkbk.nowrap)
					f.wkbk.write('D', my_commodity.combined_local_duty, f.wkbk.nowrap)
					f.wkbk.write('E', my_commodity.applied_duty, f.wkbk.nowrap)
				f.wkbk.write('F', my_commodity.product_line_suffix, f.wkbk.center)
				f.wkbk.write('G', str(my_commodity.indents), f.wkbk.center)
				f.wkbk.write('H', str(my_commodity.leaf), f.wkbk.center)
		###########################################################################
		## Write the main document
		###########################################################################

		sOut = ""
		if self.new_section == True:
			sHeading1XML = app.sHeading1XML
			sHeading1XML = sHeading1XML.replace("{HEADINGa}", "Section " + self.section_numeral)
			sHeading1XML = sHeading1XML.replace("{HEADINGb}", self.section_title)
			sOut += sHeading1XML
			if self.section_notes != "":
				sOut += self.section_notesHeading
				sOut += f.fmtMarkdown(self.section_notes)

		sHeading2XML = app.sHeading2XML
		sHeading2XML = sHeading2XML.replace("{CHAPTER}", "Chapter " + self.chapter_string)
		sHeading2XML = sHeading2XML.replace("{HEADING}", self.chapter_description)
		sOut += sHeading2XML

		if app.sDocumentType == "classification":
			sChap = app.sHeading3XML.replace("{HEADING}", "Chapter Notes")
			sOut += sChap
			sOut += f.fmtMarkdown(self.chapter_notes)

		sTableXML = app.sTableXML
		#There are special columns where the width of the description needs to be big
		if self.chapter_id in (3, 15, 22, 29, 32, 38, 39, 44, 64, 70, 72, 84, 85):
			width_list = [650, 900, 800, 2650]
		else:
			width_list = [650, 1150, 900, 2200]

		sTableXML = sTableXML.replace("{WIDTH_CLASSIFICATION}", str(width_list[0]))
		sTableXML = sTableXML.replace("{WIDTH_DUTY}",			str(width_list[1]))
		sTableXML = sTableXML.replace("{WIDTH_NOTES}",			str(width_list[2]))
		sTableXML = sTableXML.replace("{WIDTH_DESCRIPTION}",	str(width_list[3]))

		sTableXML = sTableXML.replace("{TABLEBODY}", table_content)

		sOut += sTableXML
		sDocumentXML = app.sDocumentXML
		sDocumentXML = sDocumentXML.replace("{BODY}", sOut)

		# Final replaces on the super and subscripts
		sDocumentXML = sDocumentXML.replace("{TITLE1}", self.document_title.upper())
		sDocumentXML = re.sub("<w:t>(.*)m2</w:t>", "<w:t>\g<1>m</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"superscript\"/></w:rPr><w:t>2</w:t>", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("<w:t>(.*)m3</w:t>", "<w:t>\g<1>m</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"superscript\"/></w:rPr><w:t>3</w:t>", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("<w:t>(.*)K2O</w:t>", "<w:t>\g<1>K</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>2</w:t></w:r><w:r><w:t>O</w:t>", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("<w:t>(.*)H2O2</w:t>", "<w:t>\g<1>H</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>2</w:t></w:r><w:r><w:t>O</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>2</w:t>", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("<w:t>(.*)P2O5</w:t>", "<w:t>\g<1>P</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>2</w:t></w:r><w:r><w:t>O</w:t></w:r><w:r><w:rPr><w:vertAlign w:val=\"subscript\"/></w:rPr><w:t>5</w:t>", sDocumentXML, flags=re.MULTILINE)
		
		# Subscripts
		sDocumentXML = re.sub("@(.)", '</w:t></w:r><w:r><w:rPr><w:vertAlign w:val="subscript"/></w:rPr><w:t>\\1</w:t></w:r><w:r><w:t>', sDocumentXML, flags=re.MULTILINE)

		# Missing commas
		sDocumentXML = re.sub("([0-9]),([0-9]) kg", "\\1.\\2 kg", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]) Kg", "\\1.\\2 kg", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]) C", "\\1.\\2 C", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9])kg", "\\1.\\2kg", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) g", "\\1.\\2 g", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3})g", "\\1.\\2g", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) dl", "\\1.\\2 dl", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) m", "\\1.\\2 m", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3})m", "\\1.\\2m", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) decitex", "\\1.\\2 decitex", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) l", "\\1.\\2 l", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) kW", "\\1.\\2 kW", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) W", "\\1.\\2 W", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) V", "\\1.\\2 V", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) Ah", "\\1.\\2 Ah", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) bar", "\\1.\\2 bar", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) cm", "\\1.\\2 cm", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) Nm", "\\1.\\2 Nm", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) kV", "\\1.\\2 kV", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) kHz", "\\1.\\2 kHz", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) kV", "\\1.\\2 kV", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) MHz", "\\1.\\2 MHz", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) μm", "\\1.\\2 μm", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) Ohm", "\\1.\\2 Ohm", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) dB", "\\1.\\2 dB", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("([0-9]),([0-9]{1,3}) kvar", "\\1.\\2 kvar", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("±([0-9]),([0-9]{1,3})", "±\\1.\\2", sDocumentXML, flags=re.MULTILINE)
		sDocumentXML = re.sub("€ ([0-9]{1,3}),([0-9]{1,3})", "€ \\1.\\2", sDocumentXML, flags=re.MULTILINE)


		sFileName = os.path.join(app.MODEL_DIR, "word")
		sFileName = os.path.join(sFileName, "document.xml")


		file = codecs.open(sFileName, "w", "utf-8")
		file.write(sDocumentXML)
		file.close()

		#print ("Creating document")

		###########################################################################
		## Finally, ZIP everything up
		###########################################################################

		f.zipdir(self.word_filename)

	def getChapterBasics(self):
		BASE_DIR     = os.path.dirname(os.path.realpath(__file__))
		OUTPUT_DIR = os.path.join(BASE_DIR, "output")
		OUTPUT_DIR = os.path.join(OUTPUT_DIR, app.sDocumentType)

		filename = app.sDocumentType + "_" + self.chapter_string + ".docx"
		self.word_filename = os.path.join(OUTPUT_DIR, filename)
		if (app.sDocumentType == "classification"):
			self.document_title = "UK Goods Classification"
		else:
			self.document_title = "UK Goods Schedule"

	def getSupplementaryUnits(self):
		###############################################################
		# Get the supplementary units
		sql = """SELECT m.goods_nomenclature_item_id, mcc.measurement_unit_code, mcc.measurement_unit_qualifier_code FROM ml.v5_brexit_day m, measure_components mcc
		WHERE measure_type_id IN ('109', '110')
		AND m.measure_sid = mcc.measure_sid
		AND goods_nomenclature_item_id LIKE '""" + self.chapter_string + """%'"""
		curSupplementary = app.conn.cursor()
		curSupplementary.execute(sql)
		rowsSupplementary = curSupplementary.fetchall()
		self.supplementary_unit_list = list(rowsSupplementary)

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
		AND fagn.goods_nomenclature_item_id LIKE '""" + self.chapter_string + """%'
		AND ft.application_code IN ('1', '2')
		AND fagn.validity_start_date < CURRENT_DATE
		AND (fagn.validity_end_date > CURRENT_DATE OR fagn.validity_end_date IS NULL)
		AND gn.validity_start_date < CURRENT_DATE
		AND (gn.validity_end_date > CURRENT_DATE OR gn.validity_end_date IS NULL)
		ORDER BY 1, 2"""
		cur = app.conn.cursor()
		cur.execute(sql)
		rows_foonotes = cur.fetchall()
		self.footnote_list = list(rows_foonotes)
		self.footnote_listUnique = []
		for x in self.footnote_list:
			blFound = False
			for y in self.footnote_listUnique:
				if x[1] == y[0]:
					blFound = True
					break
			if blFound == False:
				self.footnote_listUnique.append([x[1], f.formatFootnote(x[2])])

	def getChapterDescription(self):
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

	def getSection(self):
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



	def getSectionNotes(self):
		###############################################################
		# Get the section notes
		# Relevant to the classification only
		sql = """SELECT content FROM section_notes WHERE section_id = '""" + str(self.sSectionID) + """'"""
		cur = app.conn.cursor()
		cur.execute(sql)
		if cur.rowcount == 0:
			self.section_notesHeading = ""
			self.section_notes        = ""
		else:
			row = cur.fetchone()
			self.section_notes        = row[0]
			self.section_notesHeading = app.sHeading3XML
			self.section_notesHeading = self.section_notesHeading.replace("{HEADING}", "There are important section notes for this part of the tariff:")


	def getChapterNotes(self):
		###############################################################
		# Get the chapter notes
		# Relevant to the classification only
		sql = "SELECT content FROM chapter_notes WHERE chapter_id = '" + self.chapter_string + "'"
		cur = app.conn.cursor()
		cur.execute(sql)
		row = cur.fetchone()
		try:
			self.chapter_notes = row[0]
		except:
			self.chapter_notes = ""

	def get_mfn_duties(self):
		###############################################################
		# Get the duties
		# print ("Getting mfn duties")

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
		#print (sql, app.DBASE)

		cur = app.conn.cursor()
		cur.execute(sql)
		rows_duties = cur.fetchall()

		# Do a pass through the duties table and create a full duty expression
		self.duty_list = []
		for row in rows_duties:
			# print ("Found a duty")
			
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

		#print (len(self.duty_list))

		# sys.exit()

	def get_local_duties(self):
		###############################################################
		# Get local duties
		sql = """SELECT m.goods_nomenclature_item_id, m.additional_code_type_id, m.additional_code_id,
		m.measure_type_id, mc.duty_expression_id, mc.duty_amount, mc.monetary_unit_code,
		mc.measurement_unit_code, mc.measurement_unit_qualifier_code, m.measure_sid /*,
		m.validity_start_date, m.validity_end_date, m.geographical_area_id*/
		FROM measure_components mc, ml.v5 m
		WHERE mc.measure_sid = m.measure_sid
		AND LEFT(m.goods_nomenclature_item_id, 2) = '""" + self.chapter_string + """'
		AND m.measure_type_id IN ('142', '145')
		and m.geographical_area_id = 'IL'
		ORDER BY m.goods_nomenclature_item_id, m.measure_type_id, m.measure_sid, mc.duty_expression_id
		"""
		#print (sql, app.DBASE)
		#sys.exit()

		cur = app.conn.cursor()
		cur.execute(sql)
		rows_duties = cur.fetchall()

		# Do a pass through the duties table and create a full duty expression
		self.local_duty_list = []
		for row in rows_duties:
			
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
			self.local_duty_list.append(oDuty)


	def get_local_quotas(self):
		###############################################################
		# Get local quotas
		sql = """
		SELECT m.goods_nomenclature_item_id
		FROM ml.v5 m
		where LEFT(m.goods_nomenclature_item_id, 2) = '""" + self.chapter_string + """'
		AND m.measure_type_id IN ('143', '146')
		and m.geographical_area_id = 'IL'
		ORDER BY m.goods_nomenclature_item_id, m.measure_type_id, m.measure_sid
		"""
		#print (sql, app.DBASE)
		#sys.exit()

		cur = app.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()

		# Do a pass through the duties table and create a full duty expression
		self.quota_list = []
		for row in rows:
			commodity_code = f.mstr(row[0])
			self.quota_list.append(commodity_code)

	def get_applied_duties(self):
		for comm in self.commodity_list:
			if comm.leaf == 1:
				duty_len			= len(comm.combined_duty)
				duty_percentage_pos = comm.combined_duty.find("%")
				duty_euro_pos		= comm.combined_duty.find("€")
				if duty_percentage_pos != -1 and duty_percentage_pos < duty_euro_pos:
					duty_advalorem = comm.combined_duty[:duty_percentage_pos]
				else:
					duty_advalorem = 999

				local_duty_len				= len(comm.combined_local_duty)
				local_duty_percentage_pos	= comm.combined_local_duty.find("%")
				local_duty_euro_pos			= comm.combined_duty.find("€")
				if local_duty_percentage_pos != -1 and local_duty_percentage_pos < local_duty_euro_pos:
					local_duty_advalorem = comm.combined_local_duty[:local_duty_percentage_pos]
				else:
					local_duty_advalorem = 999

				if (float(local_duty_advalorem) < float(duty_advalorem)) and comm.combined_local_duty != "":
					comm.applied_duty = comm.combined_local_duty
					if comm.has_quota:
						comm.applied_duty += " Quota available"
				else:
					comm.applied_duty = comm.combined_duty
			
			comm.applied_duty = comm.applied_duty.strip()
