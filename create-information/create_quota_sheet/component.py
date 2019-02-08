import functions

class component(object):
	def __init__(self, sMeasureSID, iDutyAmount, sMonetaryUnitCode, iDutyExpressionID, sMonetaryUnitDescription, sMonetaryUnitQualifierDescription, sDutyExpressionDescription, sActive):
		# Get parameters from instantiator
		self.sMeasureSID                       = sMeasureSID
		self.iDutyAmount                       = functions.fltNone(iDutyAmount)
		self.sMonetaryUnitCode                 = functions.strNone(sMonetaryUnitCode)
		self.iDutyExpressionID                 = iDutyExpressionID
		self.sMonetaryUnitDescription          = functions.strNone(sMonetaryUnitDescription)
		self.sMonetaryUnitQualifierDescription = functions.strNone(sMonetaryUnitQualifierDescription)
		self.sDutyExpressionDescription        = functions.strNone(sDutyExpressionDescription)
		self.sActive                           = functions.strNone(sActive)
		
		self.sExpression                       = ""
		self.concatenateFields()		
	
	def concatenateFields(self):
		s = ""
		
		#print (self.sMeasureSID)
		if self.iDutyAmount > 0:
			s += "{:.2f}".format(self.iDutyAmount)
			if self.sDutyExpressionDescription != "":
				s = self.addDed(s)
				if self.sMonetaryUnitDescription != "":
					s += " / " + self.sMonetaryUnitDescription
					if self.sMonetaryUnitQualifierDescription != "":
						s += " / " + self.sMonetaryUnitQualifierDescription
		elif self.iDutyAmount == -1:
			if self.sDutyExpressionDescription != "":
				s = self.addDed(s)
				if self.sMonetaryUnitDescription != "":
					s += " / " + self.sMonetaryUnitDescription
					if self.sMonetaryUnitQualifierDescription != "":
						s += " / " + self.sMonetaryUnitQualifierDescription
		else:
			s = "0.00%"

		s = functions.mShorten(s)
		s = "[" + self.iDutyExpressionID + "] " + s.strip()
		self.sExpression = s
		
	def addDed(self, s):
		s = str(s)
		if s == "None":
			s = ""
		sWorking = ""
		s2 = ""
		sModifier = ""
		if self.sDutyExpressionDescription.find("+ "):
			sWorking = "+ "
		elif self.sDutyExpressionDescription.find("minus"):
			sWorking = "- "
		
		s2 = self.sDutyExpressionDescription.replace("+ ", "")
		s2 = s2.replace("minus ", "")
		
		if self.sMonetaryUnitCode != "":
			sModifier = self.sMonetaryUnitCode
		else:
			if self.iDutyAmount != -1:
				sModifier = "%"
				
		if s2 == "% or amount":
			s2 = ""
			
		if s2 == "Maximum" or s2 == "Minimum":
			sWorking = sWorking + s2 + " " + s + " " + sModifier
		else:
			sWorking = sWorking + " " + str(s) + " " + str(sModifier) + " " + s2
		
		sWorking = sWorking.replace("  ", " ")
	   
		return (sWorking)

