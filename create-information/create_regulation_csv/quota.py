import functions
from datetime import datetime
from dateutil import parser

class quota(object):
	def __init__(self, order_number):
		
		# Get parameters from instantiator
		self.order_number		= order_number
		self.measure_count		= 0
		self.measure_type		= ""
		self.commodity_list		= []
		self.date_set			= set()
		self.special_text		= ""

	def get_specials(self):
		if len(self.date_set) > 0:
			for d in self.date_set:
				ar = d.split("-")
				valid_from	= ar[0].strip()
				valid_to	= ar[1].strip()
				if valid_to != "no end date":
					dt_from	= parser.parse(valid_from)
					dt_to	= parser.parse(valid_to)
					diff = (dt_to - dt_from)
					diff2 = diff.days + 1
					if diff2 < 365:
						self.special_text += "Quota contains periods shorter than 365 days - check what needs cloning"
						break
				else:
					pass
					
		