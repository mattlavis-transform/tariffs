import functions

class footnote(object):
	def __init__(self, measure_sid, footnote_type_id, footnote_id, footnote_description, footnote_type_description):
		# Get parameters from instantiator
		self.measure_sid				= measure_sid
		self.footnote_type_id			= footnote_type_id
		self.footnote_id				= footnote_id
		self.footnote_description		= footnote_description
		self.footnote_type_description	= footnote_type_description
		self.footnote_concat			= self.footnote_type_id + self.footnote_id
		
		self.sFootnoteFull            	= ""

		self.concatenateFields()
		if not(self.footnote_concat in functions.app.footnote_list):
			functions.app.footnote_count += 1

		functions.app.footnote_list.add (self.footnote_concat)
		
	def concatenateFields(self):
		s = ""
		s += self.footnote_type_id
		s += self.footnote_id + ": (" + self.footnote_type_description + ") " + self.footnote_description
		self.sFootnoteFull = s