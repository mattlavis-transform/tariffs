import re

import functions

class tableRow(object):
	def __init__(self, sCommodityCode = "", sDescription = "", sProductLineSuffix = "", indents = 0, leaf = 0):
		# Get parameters from instantiator
		self.sCommodityCode           = sCommodityCode
		self.sDescription             = sDescription
		self.sProductLineSuffix       = sProductLineSuffix
		self.indents                 = indents
		self.leaf                     = leaf

		self.blDutySetOnMyLevel       = False
		self.blSuspensionSetOnMyLevel = False
		self.sDuty                    = ""
		self.sDutyString              = ""
		self.sNotes                   = ""
		self.sLegalBase               = ""
		self.sSuspensionDuty          = ""
		self.sMeasureTypeID           = ""
		self.sMeasureTypeDescription  = ""
		
		self.sDutyLast                = ""
		self.iDutyLastIndent          = -1

		self.sSupplementaryUnit       = ""
		
		self.formatDescription()
		self.getSignificantFigures()
		self.getIndentString()
		self.formatCommodityCode()

	def checkforSIV(self, app):
		if self.sCommodityCode in app.siv_list:
			if self.sCommodityCodeFormatted != "":
				self.sDutyString = "Formula"
				self.sNotes      = "Entry Price"

	def checkforVessel(self, app):
		if self.sCommodityCode in app.vessels_list:
			if self.sCommodityCodeFormatted != "":
				self.sNotes      = "Vessels / platforms relief"

	def checkforCivilAir(self, app):
		if self.sCommodityCode in app.civilair_list:
			if self.sCommodityCodeFormatted != "":
				self.sNotes      = "Civil aircraft relief"

	def checkforAirworthiness(self, app):
		if self.sCommodityCode in app.airworthiness_list:
			if self.sCommodityCodeFormatted != "":
				self.sNotes      = "Airworthiness relief"

	def checkforAircraft(self, app):
		if self.sCommodityCode in app.aircraft_list:
			if self.sCommodityCodeFormatted != "":
				self.sNotes      = "Aircraft relief"

	def checkforPharmaceuticals(self, app):
		if self.sCommodityCode in app.pharmaceuticals_list:
			if self.sCommodityCodeFormatted != "":
				self.sNotes      = "Pharmaceuticals relief"

	def apply(self, sCommodityCode, sDescription, sProductLineSuffix, indents, leaf):
		self.sCommodityCode           = sCommodityCode
		self.sDescription             = sDescription
		self.sProductLineSuffix       = sProductLineSuffix
		self.indents                 = indents
		self.leaf                     = leaf
	
	def checkForFootnotes(self, lstFootnotes):
		pass
		if 1 > 2:
			for l in lstFootnotes:
				# fagn.goods_nomenclature_item_id, fagn.footnote_type, fagn.footnote_id, fd.description as footnote_description
				sCommodityCode = l[0]
				sFootnote      = l[1]
				sDescription   = l[2]
				if (sCommodityCode == self.sCommodityCode):
					self.sNotes = "See note " + sFootnote
					break
	
	def applySuspension(self):
		if self.blSuspensionSetOnMyLevel:
			self.sDuty  = self.sSuspensionDuty
			if self.sProductLineSuffix == "80":
				self.sNotes     = self.sNotes + self.sMeasureTypeDescription + ". "
				self.sLegalBase = "12"
		else:
			if self.sMeasureTypeID == "103": # Third country duty (MFNs)
				self.sLegalBase = "8"
			elif self.sMeasureTypeID in ("105", "107"): # Third country duty under end use / authorised use
				self.sNotes     = self.sNotes + self.sMeasureTypeDescription + ". "
				self.sLegalBase = "19"
			else:
				self.sNotes     = self.sNotes + self.sMeasureTypeDescription + ". "
				self.sLegalBase = "8"
		
		if self.sLegalBase == "12":
			self.sNotes = self.sNotes + " Ends dd/mm/yy."
		

	def trimSuperfluousLegalBases(self):
		if self.sDutyString == "":
			self.sNotes     = ""
			self.sLegalBase = ""
	
	def checkForDuty(self, rdList, o):
		for rd in rdList:
			sCommodityCode = rd[0]
			sActive        = rd[7]
			if (sCommodityCode == self.sCommodityCode and sActive == "Active"):
				self.sDuty = str(rd[6])
				self.sDuty = self.sDuty.replace("  ", " ")
				self.blDutySetOnMyLevel = True
				self.sMeasureTypeID          = rd[9]
				self.sMeasureTypeDescription = rd[10]
				
				o.sDutyLast                  = self.sDuty
				o.iDutyLastIndent            = self.indents
				o.sMeasureTypeID             = self.sMeasureTypeID
				o.sMeasureTypeDescription    = self.sMeasureTypeDescription
				break
		
		if self.sDuty == "":
			if self.indents > o.iDutyLastIndent:
				self.sDuty = o.sDutyLast
				self.sMeasureTypeID          = o.sMeasureTypeID
				self.sMeasureTypeDescription = o.sMeasureTypeDescription
	
	def checkForSuspension(self, rsList, o):
		#self.sMeasureTypeDescription = ""
		self.blSuspensionSetOnMyLevel = False
		for x in range(1, len(rsList)):
			sCommodityCode = rsList[x][0]
			sActive        = rsList[x][7]
			if sCommodityCode == self.sCommodityCode and sActive == "Active":
				self.sMeasureTypeDescription  = str(rsList[x][8])
				self.sSuspensionDuty          = rsList[x][6]
				self.blSuspensionSetOnMyLevel = True
				o.sDutyLast                   = self.sDuty
				o.iDutyLastIndent             = self.indents
				break

	def formatDutyString(self):
		if (self.sProductLineSuffix == "80"):
			if (self.indents == 0) and (self.leaf == "0"):
				self.sDutyString = ""
			else:
				self.sDutyString = self.sDuty
		else:
			self.sDutyString = ""
		if self.sDutyString == "":
			self.sNotes = ""
	
	def formatDescription(self):
		self.sDescription = self.sDescription.replace("|", " ")
		self.sDescription = self.sDescription.replace("!x!", "x")
		self.sDescription = re.sub(r"\$(.)", r'</w:t></w:r><w:r><w:rPr><w:vertAlign w:val="superscript"/></w:rPr><w:t>\1</w:t></w:r><w:r><w:t xml:space="preserve">', self.sDescription)


		if self.sDescription[-3:] == "!1!":
			self.sDescription = self.sDescription[:-3]
		self.sDescription = self.sDescription.replace("\r\r", "\r")
		self.sDescription = self.sDescription.replace("\r\n", "\n")
		self.sDescription = self.sDescription.replace("\n\r", "\n")
		self.sDescription = self.sDescription.replace("\n\n", "\n")
		self.sDescription = self.sDescription.replace("\r", "\n")
		self.sDescription = self.sDescription.replace("\n", "</w:t></w:r><w:r><w:br/></w:r><w:r><w:t>")
		self.sDescription = self.sDescription.replace("!1!", "</w:t></w:r><w:r><w:br/></w:r><w:r><w:t>")
		self.sDescription = self.sDescription.replace("  ", " ")
		self.sDescription = self.sDescription.replace("!o!", chr(176))
		self.sDescription = self.sDescription.replace("\xA0", " ")
		self.sDescription = ("<w:t>-</w:t><w:tab/>" * self.indents) + "<w:t>" + self.sDescription + "</w:t>"
		if (self.indents < 2): # Make it bold
			self.sDescription = "<w:rPr><w:b/></w:rPr>" + self.sDescription

	def getSignificantFigures(self):
		if self.sCommodityCode[-8:] == '00000000':
			self.iSignificantFigures = 2
		elif self.sCommodityCode[-6:] == '000000':
			self.iSignificantFigures = 4
		elif self.sCommodityCode[-4:] == '0000':
			self.iSignificantFigures = 6
		elif self.sCommodityCode[-2:] == '00':
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
				if self.blDutySetOnMyLevel == False and self.blSuspensionSetOnMyLevel == False:
					self.blSuppressRow = True
				else:
					self.blSuppressRow = False
				
	def formatCommodityCode(self):
		self.sCommodityCode = self.sCommodityCode.replace(" anf ", " and ")
		s = self.sCommodityCode
		if self.sProductLineSuffix != "80":
			self.sCommodityCodeFormatted = ""
		else:
			if self.leaf == "1":
				if s[8:10] == "00":
					self.sCommodityCodeFormatted = s[0:4] + ' ' + s[4:6] + ' ' + s[6:8]
				else:
					self.sCommodityCodeFormatted = s[0:4] + ' ' + s[4:6] + ' ' + s[6:8] + ' ' + s[8:10]
			else:
				if s[4:10] == "000000":
					self.sCommodityCodeFormatted = s[0:4]
				elif s[6:10] == "0000":
					self.sCommodityCodeFormatted = s[0:4] + ' ' + s[4:6]
				elif s[8:10] == "00":
					self.sCommodityCodeFormatted = s[0:4] + ' ' + s[4:6] + ' ' + s[6:8]
				else:
					self.sCommodityCodeFormatted = s[0:4] + ' ' + s[4:6] + ' ' + s[6:8] + ' ' + s[8:10]

	def applySupplementaryUnit(self, rSuppList):
		for r in rSuppList:
			sCommodityCode = r[0]
			if sCommodityCode == self.sCommodityCode:
				s = functions.getMeasurementUnit(r[1])
				sq = str(r[2])
				sq2 = ""
				if sq != "None":
					sq2 = functions.getQual(sq)
				self.sSupplementaryUnit = functions.getMeasurementUnit(s) + " " + sq2
				break