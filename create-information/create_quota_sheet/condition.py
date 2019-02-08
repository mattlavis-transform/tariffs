import functions

class condition(object):
	def __init__(self, sMeasureSID, sMeasureConditionSID, sConditionCode, sConditionCodeDescription, sActionCode, sMeasureActionDescription, sConditionDutyAmount, sCertificateTypeCode, sCertificateTypeCodeDescription, sCertificateCode, sCertificateDescription, sMonetaryUnitCode, sMeasurementUnitCode, sMeasurementUnitQualifierCode, sMeasurementUnitCodeDescription, sMeasurementUnitQualifierCodeDescription):
		# Get parameters from instantiator
		self.sMeasureSID                              = sMeasureSID
		self.sMeasureConditionSID                     = sMeasureConditionSID
		self.sConditionCode                           = sConditionCode
		self.sConditionCodeDescription                = sConditionCodeDescription
		self.sActionCode                              = sActionCode
		self.sMeasureActionDescription                = sMeasureActionDescription
		self.sConditionDutyAmount                     = sConditionDutyAmount
		self.sCertificateTypeCode                     = sCertificateTypeCode
		self.sCertificateTypeCodeDescription          = sCertificateTypeCodeDescription
		self.sCertificateCode                         = sCertificateCode
		self.sCertificateDescription                  = sCertificateDescription
		self.sMonetaryUnitCode                        = sMonetaryUnitCode
		self.sMeasurementUnitCode                     = sMeasurementUnitCode
		self.sMeasurementUnitQualifierCode            = sMeasurementUnitQualifierCode
		self.sMeasurementUnitCodeDescription          = sMeasurementUnitCodeDescription
		self.sMeasurementUnitQualifierCodeDescription = sMeasurementUnitQualifierCodeDescription
		
		self.sMUQ = ""
		self.sConditionFull = ""

		self.concatenateFields()
		
	def concatenateFields(self):
		if self.sMeasurementUnitQualifierCode == None or self.sMeasurementUnitQualifierCodeDescription == None:
			self.sMUQ = ""
		else:
			self.sMUQ = self.sMeasurementUnitQualifierCode + self.sMeasurementUnitQualifierCodeDescription
			
		self.sConditionFull = ""
		# Condition statement
		self.sConditionFull += "Condition [" + self.sConditionCode + "#] " + self.sConditionCodeDescription + " : "
		# Document statement
		if self.sCertificateCode != None:
			self.sConditionFull += "Document [" + self.sCertificateTypeCode + "] "		
		# Action statement
		if self.sActionCode != None:
			self.sConditionFull += "Action [" + self.sActionCode + "] " + self.sMeasureActionDescription + " : "
		# Requirement statement
		if self.sConditionDutyAmount != None:
			self.sConditionFull += "Requirement - " + "{:.2f}".format(self.sConditionDutyAmount)
			if self.sMeasurementUnitCodeDescription != None:
				self.sConditionFull += " " + self.sMeasurementUnitCodeDescription
				if self.sMeasurementUnitQualifierCodeDescription != None:
					self.sConditionFull += " " + self.sMeasurementUnitQualifierCodeDescription
			
