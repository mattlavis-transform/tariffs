import functions as f
import re
import os
import sys
import codecs
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
		self.supplementary_unit_list = []
		self.seasonal_records = 0
		self.wide_duty = False

		print ("Creating " + app.sDocumentType + " for chapter " + self.chapter_string)

		self.getChapterBasics()

		self.getSection()
		self.getChapterDescription()
		self.getDuties()
		
		if app.sDocumentType == "classification":
			self.getSectionNotes()
			self.getChapterNotes()
		else:
			self.section_notes = ""
			self.chapter_notes = ""

	def formatChapter(self):
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
		for rw in rows:
			commodity_code    = rw[0]
			productline_suffix = f.mstr(rw[1])
			description       = rw[2]
			number_indents    = f.mnum(rw[3])
			leaf              = f.mnum(rw[4])

			my_commodity = commodity(commodity_code, description, productline_suffix, number_indents, leaf)
			commodity_list.append (my_commodity)

		for my_commodity in commodity_list:
			# Start with the duties
			for d in self.duty_list:
				#print (my_commodity.commodity_code_formatted)
				if my_commodity.commodity_code == d.commodity_code:
					if 2 > 1:
					#if my_commodity.product_line_suffix == "80":
						my_commodity.duty_list.append(d)
						my_commodity.assigned = True

			my_commodity.combineDuties()


		###########################################################################
		## Get exceptions
		###########################################################################
		if app.sDocumentType == "schedule":
			for my_commodity in commodity_list:
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
		commodity_count = len(commodity_list)

		# Okay, so this does the following
		# Loop through all 12 hierarchical tiers, starting at the bottom, which is where all of the MFN duties
		# are set. For each of those hierarchical tiers (indents), loop through the full set of commodities
		# finding any commodities whose indents match, then compare those child duties with each other:
		# if all of the duties are the same, then inherit the combined duties up to the parent
		# Rinse and repeat as you go higher up the hierarchical levels

		for indent in range(12, -1, -1):
			#print (indent)
			for loop1 in range(0, commodity_count):
				my_commodity = commodity_list[loop1]
				if my_commodity.iIndents == indent:
					for loop2 in range(loop1, -1, -1):
						antecedent = commodity_list[loop2]
						if antecedent.iIndents == (my_commodity.iIndents - 1):
							antecedent.child_duty_list.append(my_commodity.combined_duty)
							break

			for loop1 in range(0, commodity_count):
				my_commodity = commodity_list[loop1]
				if my_commodity.iIndents == indent:
					if len(my_commodity.child_duty_list) > 0:
						my_set = set(my_commodity.child_duty_list)
						if len(my_set) == 1:
							if my_commodity.combined_duty != "AU":
								my_commodity.combined_duty = my_commodity.child_duty_list[0]
								#print ("Setting at a higher level", my_commodity.commodity_code, my_commodity.combined_duty)
								# need to check this works - am passing up blanks at times

		###########################################################################
		## Check for row suppression
		###########################################################################
		
		# We should only be suppressing rows if they have 10 significant digits and their duty
		# is identical to the parent
		
		
		for loop1 in range(0, commodity_count):
			my_commodity = commodity_list[loop1]
			if my_commodity.significant_digits == 2:
				my_commodity.suppress_row = True
			elif my_commodity.significant_digits == 10:
				for loop2 in range(loop1 - 1 , -1, -1):
					antecedent = commodity_list[loop2]
					if antecedent.iIndents == (my_commodity.iIndents - 1):
						my_set = set(antecedent.child_duty_list)
						if len(my_set) == 1: # and antecedent.product_line_suffix == "80":
							if my_commodity.commodity_code not in (app.suspension_specials):
								my_commodity.suppress_row = True
						break


		###########################################################################
		## Finally, before we print, check if the duty should be suppressed
		## Hypothesis is that the duty will be suppressed if the children all
		## have the same duties, but only if they are suppressed
		###########################################################################
		for loop1 in range(0, commodity_count):
			my_commodity = commodity_list[loop1]
			if my_commodity.product_line_suffix != "80":
				my_commodity.suppress_duty = True
			elif len(set(my_commodity.child_duty_list)) == 1:
				if my_commodity.child_duty_list[0] == my_commodity.combined_duty:
					children_suppressed = False
					for loop2 in range(loop1 + 1, commodity_count):
						successor_commodity = commodity_list[loop2]
						if successor_commodity.iIndents == my_commodity.iIndents + 1:
							if successor_commodity.suppress_row == True:
								children_suppressed = True
						elif successor_commodity.iIndents <= my_commodity.iIndents:
							break
					if children_suppressed == False:
						my_commodity.suppress_duty = True

		###########################################################################
		## Output the rows to buffer
		###########################################################################

		table_content = ""
		for my_commodity in commodity_list:
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
					row_string = row_string.replace("{DUTY}",       f.surround(my_commodity.combined_duty))
					row_string = row_string.replace("{NOTES}",      my_commodity.notes_string)
				table_content += row_string
			
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
		width_list = [650, 1150, 1080, 2120]

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

	def getDuties(self):
		###############################################################
		# Get the duties
		sql = """SELECT m.goods_nomenclature_item_id, m.additional_code_type_id, m.additional_code_id,
		m.measure_type_id, mc.duty_expression_id, mc.duty_amount, mc.monetary_unit_code,
		mc.measurement_unit_code, mc.measurement_unit_qualifier_code, m.measure_sid /*,
		m.validity_start_date, m.validity_end_date, m.geographical_area_id*/
		FROM measure_components mc, ml.v5_brexit_day m
		WHERE mc.measure_sid = m.measure_sid
		AND LEFT(m.goods_nomenclature_item_id, 2) = '""" + self.chapter_string + """'
		AND m.measure_type_id IN ('103', '105') AND m.validity_start_date >= '2019-03-30'
		ORDER BY m.goods_nomenclature_item_id, m.measure_type_id, m.measure_sid, mc.duty_expression_id"""

		# print (sql)

		cur = app.conn.cursor()
		cur.execute(sql)
		rows_duties = cur.fetchall()

		# Do a pass through the duties table and create a full duty expression
		self.duty_list = []
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
			self.duty_list.append(oDuty)

