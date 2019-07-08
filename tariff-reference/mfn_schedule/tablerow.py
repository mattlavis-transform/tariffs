import re

import functions

class tableRow(object):
	def __init__(self, commodity_code = "", description = "", product_line_suffix = "", indents = 0, leaf = 0):
		# Get parameters from instantiator
		self.commodity_code           = commodity_code
		self.description             = description
		self.product_line_suffix       = product_line_suffix
		self.indents                 = indents
		self.leaf                     = leaf

		self.duty_set_on_my_level       = False
		self.suspension_set_on_my_level = False
		self.sDuty                    = ""
		self.duty_string              = ""
		self.notes                   = ""
		self.sSuspensionDuty          = ""
		self.measure_type_id           = ""
		self.measure_type_description  = ""
		
		self.duty_last                = ""
		self.duty_last_indent          = -1

		self.sSupplementaryUnit       = ""
		
		self.formatDescription()
		self.getSignificantFigures()
		self.getIndentString()
		self.formatCommodityCode()

	def checkforSIV(self, app):
		if self.commodity_code in app.siv_list:
			if self.commodity_codeFormatted != "":
				self.duty_string = "Formula"
				self.notes      = "Entry Price"

	def checkforVessel(self, app):
		if self.commodity_code in app.vessels_list:
			if self.commodity_codeFormatted != "":
				self.notes      = "Vessels / platforms relief"

	def checkforCivilAir(self, app):
		if self.commodity_code in app.civilair_list:
			if self.commodity_codeFormatted != "":
				self.notes      = "Civil aircraft relief"

	def checkforAirworthiness(self, app):
		if self.commodity_code in app.airworthiness_list:
			if self.commodity_codeFormatted != "":
				self.notes      = "Airworthiness relief"

	def checkforAircraft(self, app):
		if self.commodity_code in app.aircraft_list:
			if self.commodity_codeFormatted != "":
				self.notes      = "Aircraft relief"

	def checkforPharmaceuticals(self, app):
		if self.commodity_code in app.pharmaceuticals_list:
			if self.commodity_codeFormatted != "":
				self.notes      = "Pharmaceuticals relief"

	def apply(self, commodity_code, description, product_line_suffix, indents, leaf):
		self.commodity_code           = commodity_code
		self.description             = description
		self.product_line_suffix       = product_line_suffix
		self.indents                 = indents
		self.leaf                     = leaf
	
	def checkForFootnotes(self, lstFootnotes):
		pass
		if 1 > 2:
			for l in lstFootnotes:
				# fagn.goods_nomenclature_item_id, fagn.footnote_type, fagn.footnote_id, fd.description as footnote_description
				commodity_code = l[0]
				sFootnote      = l[1]
				description   = l[2]
				if (commodity_code == self.commodity_code):
					self.notes = "See note " + sFootnote
					break
	
	def checkForDuty(self, rdList, o):
		for rd in rdList:
			commodity_code = rd[0]
			sActive        = rd[7]
			if (commodity_code == self.commodity_code and sActive == "Active"):
				self.sDuty = str(rd[6])
				self.sDuty = self.sDuty.replace("  ", " ")
				self.duty_set_on_my_level = True
				self.measure_type_id          = rd[9]
				self.measure_type_description = rd[10]
				
				o.duty_last                  = self.sDuty
				o.duty_last_indent            = self.indents
				o.measure_type_id             = self.measure_type_id
				o.measure_type_description    = self.measure_type_description
				break
		
		if self.sDuty == "":
			if self.indents > o.duty_last_indent:
				self.sDuty = o.duty_last
				self.measure_type_id          = o.measure_type_id
				self.measure_type_description = o.measure_type_description
	
	def checkForSuspension(self, rsList, o):
		#self.measure_type_description = ""
		self.suspension_set_on_my_level = False
		for x in range(1, len(rsList)):
			commodity_code = rsList[x][0]
			sActive        = rsList[x][7]
			if commodity_code == self.commodity_code and sActive == "Active":
				self.measure_type_description  = str(rsList[x][8])
				self.sSuspensionDuty          = rsList[x][6]
				self.suspension_set_on_my_level = True
				o.duty_last                   = self.sDuty
				o.duty_last_indent             = self.indents
				break

	def formatDutyString(self):
		if (self.product_line_suffix == "80"):
			if (self.indents == 0) and (self.leaf == "0"):
				self.duty_string = ""
			else:
				self.duty_string = self.sDuty
		else:
			self.duty_string = ""
		if self.duty_string == "":
			self.notes = ""
	
	def formatDescription(self):
		self.description = self.description.replace("|", " ")
		self.description = self.description.replace("!x!", "x")
		self.description = re.sub(r"\$(.)", r'</w:t></w:r><w:r><w:rPr><w:vertAlign w:val="superscript"/></w:rPr><w:t>\1</w:t></w:r><w:r><w:t xml:space="preserve">', self.description)


		if self.description[-3:] == "!1!":
			self.description = self.description[:-3]
		self.description = self.description.replace("\r\r", "\r")
		self.description = self.description.replace("\r\n", "\n")
		self.description = self.description.replace("\n\r", "\n")
		self.description = self.description.replace("\n\n", "\n")
		self.description = self.description.replace("\r", "\n")
		self.description = self.description.replace("\n", "</w:t></w:r><w:r><w:br/></w:r><w:r><w:t>")
		self.description = self.description.replace("!1!", "</w:t></w:r><w:r><w:br/></w:r><w:r><w:t>")
		self.description = self.description.replace("  ", " ")
		self.description = self.description.replace("!o!", chr(176))
		self.description = self.description.replace("\xA0", " ")
		self.description = ("<w:t>-</w:t><w:tab/>" * self.indents) + "<w:t>" + self.description + "</w:t>"
		if (self.indents < 2): # Make it bold
			self.description = "<w:rPr><w:b/></w:rPr>" + self.description

	def getSignificantFigures(self):
		if self.commodity_code[-8:] == '00000000':
			self.iSignificantFigures = 2
		elif self.commodity_code[-6:] == '000000':
			self.iSignificantFigures = 4
		elif self.commodity_code[-4:] == '0000':
			self.iSignificantFigures = 6
		elif self.commodity_code[-2:] == '00':
			self.iSignificantFigures = 8
		else:
			self.iSignificantFigures = 10
		
	def getIndentString(self):
		oIndents      = [0, 113, 227, 340, 454, 567, 680, 794, 907, 1020, 1134, 1247, 1361]
		self.sIndentString = "<w:ind w:left=\"" + str(oIndents[self.indents]) + "\" w:hanging=\"" + str(oIndents[self.indents]) + "\"/>"

	def checkForRowSuppression(self):
	# Work out whether to suppress the row or not
		if self.commodity_code[2:10] == "00000000":
			self.blSuppressRow = True
		else:
			if self.iSignificantFigures != 10: # Never suppress the row if there are fewer than 10 significant digits
				self.blSuppressRow = False
			else:
				if self.duty_set_on_my_level == False and self.suspension_set_on_my_level == False:
					self.blSuppressRow = True
				else:
					self.blSuppressRow = False
				
	def formatCommodityCode(self):
		self.commodity_code = self.commodity_code.replace(" anf ", " and ")
		s = self.commodity_code
		if self.product_line_suffix != "80":
			self.commodity_codeFormatted = ""
		else:
			if self.leaf == "1":
				if s[8:10] == "00":
					self.commodity_codeFormatted = s[0:4] + ' ' + s[4:6] + ' ' + s[6:8]
				else:
					self.commodity_codeFormatted = s[0:4] + ' ' + s[4:6] + ' ' + s[6:8] + ' ' + s[8:10]
			else:
				if s[4:10] == "000000":
					self.commodity_codeFormatted = s[0:4]
				elif s[6:10] == "0000":
					self.commodity_codeFormatted = s[0:4] + ' ' + s[4:6]
				elif s[8:10] == "00":
					self.commodity_codeFormatted = s[0:4] + ' ' + s[4:6] + ' ' + s[6:8]
				else:
					self.commodity_codeFormatted = s[0:4] + ' ' + s[4:6] + ' ' + s[6:8] + ' ' + s[8:10]

	def applySupplementaryUnit(self, rSuppList):
		for r in rSuppList:
			commodity_code = r[0]
			if commodity_code == self.commodity_code:
				s = functions.getMeasurementUnit(r[1])
				sq = str(r[2])
				sq2 = ""
				if sq != "None":
					sq2 = functions.getQual(sq)
				self.sSupplementaryUnit = functions.getMeasurementUnit(s) + " " + sq2
				break