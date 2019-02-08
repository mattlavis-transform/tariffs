import functions

class footnote(object):
	def __init__(self, sMeasureSID, sFootnoteTypeID, sFootnoteID, sFootnoteDescription, sFootnoteTypeDescription):
		# Get parameters from instantiator
		self.sMeasureSID              = sMeasureSID
		self.sFootnoteTypeID          = sFootnoteTypeID
		self.sFootnoteID              = sFootnoteID
		self.sFootnoteDescription     = sFootnoteDescription
		self.sFootnoteTypeDescription = sFootnoteTypeDescription
		
		self.sFootnoteFull            = ""

		self.concatenateFields()
		
	def concatenateFields(self):
		s = ""
		s += self.sFootnoteTypeID
		s += self.sFootnoteID + ": (" + self.sFootnoteTypeDescription + ") " + self.sFootnoteDescription
		self.sFootnoteFull = s