import functions

class measure(object):
	def __init__(self, sMeasureTypeDescription, sMeasureTypeID, sMeasureSID, sGeographicalAreaID, sGoodsNomenclatureItemID, sAdditionalCodeTypeID, sAdditionalCodeID, sValidityStartDate, sValidityEndDate, sOrderNumber, sAdditionalCodeDescription, sGeographicalAreaDescription):
		# Get parameters from instantiator
		self.sMeasureTypeDescription      = sMeasureTypeDescription
		self.sMeasureTypeID               = sMeasureTypeID
		self.sMeasureSID                  = sMeasureSID
		self.sGeographicalAreaID          = sGeographicalAreaID
		self.sGoodsNomenclatureItemID     = sGoodsNomenclatureItemID
		self.sAdditionalCodeTypeID        = sAdditionalCodeTypeID
		self.sAdditionalCodeID            = sAdditionalCodeID
		self.sValidityStartDate           = str(sValidityStartDate)
		self.sValidityEndDate             = str(sValidityEndDate)
		self.sOrderNumber                 = sOrderNumber
		self.sAdditionalCodeDescription   = sAdditionalCodeDescription
		self.sGeographicalAreaDescription = sGeographicalAreaDescription
		self.sMeasureTypeFull             = ""
		self.sAdditionalCodeFull          = ""
		self.sGeographicalAreaFull        = ""
		self.sValidityDates               = ""
		self.sOrderNumber                 = ""
		self.sComponents                  = ""
		self.sComponentsExcel             = ""
		self.sConditions                  = ""
		self.sConditionsExcel             = ""
		self.sFootnotes                   = ""

		self.sDelimiter                   = "|"
		self.sDelimiterExcel              = "\n"
		
		self.concatenateFields()
		
	def concatenateFields(self):
		self.sMeasureTypeFull = "[" + str(self.sMeasureTypeID) + "] " + str(self.sMeasureTypeDescription)
		if str(self.sAdditionalCodeTypeID) == "None":
			self.sAdditionalCodeFull = ""
		else:
			self.sAdditionalCodeFull = "[" + str(self.sAdditionalCodeTypeID) + str(self.sAdditionalCodeID) + "] " + str(self.sAdditionalCodeDescription)
		self.sGeographicalAreaFull = "[" + str(self.sGeographicalAreaID) + "] " + str(self.sGeographicalAreaDescription)
		
		if self.sValidityStartDate != "None":
			#self.sValidityDates = self.sValidityStartDate
			self.sValidityDates = functions.fmtDate2(self.sValidityStartDate)
			if self.sValidityEndDate != "None":
				self.sValidityDates += " - " + functions.fmtDate2(self.sValidityEndDate)

	def addComponents(self, lstMeasureComponents):
		for mc in lstMeasureComponents:
			if mc.sMeasureSID == self.sMeasureSID:
				self.sComponents += mc.sExpression
				self.sComponents += " " + self.sDelimiter + " "

		self.sComponents = self.sComponents.strip()
		self.sComponents = self.sComponents.strip(self.sDelimiter)
		self.sComponents = self.sComponents.strip()
		
		self.sComponentsExcel = self.sComponents.replace(" " + self.sDelimiter + " ", self.sDelimiterExcel)

	def addFootnotes(self, lstFootnotes):
		for f in lstFootnotes:
			if f.sMeasureSID == self.sMeasureSID:
				self.sFootnotes += f.sFootnoteFull
				self.sFootnotes += " " + self.sDelimiter + " "
		self.sFootnotes = self.sFootnotes.strip()
		self.sFootnotes = self.sFootnotes.strip(self.sDelimiter)
		self.sFootnotes = self.sFootnotes.strip()

		self.sComponentsExcel = self.sComponents.replace(" " + self.sDelimiter + " ", self.sDelimiterExcel)

	def addConditions(self, lstConditions):
		i = 1
		for c in lstConditions:
			if c.sMeasureSID == self.sMeasureSID:
				self.sConditions += c.sConditionFull.replace("#", str(i))
				self.sConditions += self.sDelimiter + self.sDelimiter
				i = i + 1
		self.sConditions = self.sConditions.strip()
		self.sConditions = self.sConditions.strip(self.sDelimiter)
		self.sConditions = self.sConditions.strip()

		self.sConditionsExcel = self.sConditions.replace(" " + self.sDelimiter + " ", self.sDelimiterExcel)
		self.sConditionsExcel = self.sConditionsExcel.replace(self.sDelimiter, self.sDelimiterExcel)
		self.sConditionsExcel = self.sConditionsExcel.replace(" : " , "\n")
