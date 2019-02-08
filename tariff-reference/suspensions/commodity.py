import urllib.request, json, sys
import functions as f
import glob as g
from hierarchy import hierarchy

class commodity(object):
	def __init__(self, measure_sid, goods_nomenclature_item_id, validity_start_date):
		self.measure_sid				= measure_sid
		self.goods_nomenclature_item_id	= goods_nomenclature_item_id
		self.validity_start_date		= validity_start_date

		self.description	= ""
		self.subheading		= self.goods_nomenclature_item_id[0:4]
		self.ancestors		= []
		self.hierarchy		= ""
		self.end_date		= ""

		self.duty_list		= []
		self.get_end_date()

	def get_end_date(self):
		self.end_date = "Missing end date"
		for item in g.app.david_owen_list:
			self.include = False
			if item.goods_nomenclature_item_id == self.goods_nomenclature_item_id:
				self.include = True
				self.end_date = item.end_date
				break

		if g.app.include_do_only == False:
			self.include = True

	def get_hierarchy(self):
		# Find the right hierarchy in the list of subheading_hierarchies
		for h in g.app.list_of_hierarchies:
			if h.subheading == self.subheading:
				#print (h.subheading, "Found")
				#print (h.hierarchy_list)
				cnt = len(h.hierarchy_list)
				for i in range(cnt-1, 0, -1):
					item = h.hierarchy_list[i]
					if item.goods_nomenclature_item_id == self.goods_nomenclature_item_id and item.producline_suffix == "80":
						current_indent = item.number_indents
						self.ancestors.append (self.cleanse(item.description))
						my_index = i
						break

				for i in range(my_index - 1, 0, -1):
					item = h.hierarchy_list[i]
					if item.number_indents < current_indent:
						self.ancestors.append (self.cleanse(item.description))
						current_indent = item.number_indents

				self.ancestors.append(self.cleanse(h.hierarchy_list[0].description))
				#print (self.ancestors)
				self.ancestors.reverse()
				#print (self.ancestors)


				index = 1
				for ancestor in self.ancestors:
					if index == 1:
						self.hierarchy += g.app.sTier1XML.replace("[DESCRIPTION]", ancestor)
					elif index == 2:
						self.hierarchy += g.app.sTier2XML.replace("[DESCRIPTION]", ancestor)
					elif index == 3:
						self.hierarchy += g.app.sTier3XML.replace("[DESCRIPTION]", ancestor)
					elif index == 4:
						self.hierarchy += g.app.sTier4XML.replace("[DESCRIPTION]", ancestor)
					elif index == 5:
						self.hierarchy += g.app.sTier5XML.replace("[DESCRIPTION]", ancestor)
					elif index == 6:
						self.hierarchy += g.app.sTier6XML.replace("[DESCRIPTION]", ancestor)
					elif index == 7:
						self.hierarchy += g.app.sTier7XML.replace("[DESCRIPTION]", ancestor)

					index += 1
					
				#sys.exit()

	def cleanse(self, s):
		s = s.replace("|", " ")
		s = s.replace("  ", " ")
		return s

	def old_get_hierarchy(self):
		app = g.app
		with urllib.request.urlopen("https://www.trade-tariff.service.gov.uk/trade-tariff/commodities/" + self.goods_nomenclature_item_id + ".json#import") as url:
			data = json.loads(url.read().decode())

		self.description	= data["description"]
		self.chapter		= data["chapter"]["formatted_description"]
		for ancestor in data["ancestors"]:
			self.ancestors.append (ancestor["description"])

		self.hierarchy = ""
		self.hierarchy += app.sTier1XML.replace("[DESCRIPTION]", self.chapter)

	def combineDuties(self):
		self.combined_duty      = ""

		self.measure_list         = []
		self.measure_type_list    = []
		self.additional_code_list = []

		for d in self.duty_list:
			self.measure_type_list.append(d.measure_type_id)
			self.measure_list.append(d.measure_sid)
			self.additional_code_list.append(d.additional_code_id)

		measure_type_list_unique    = set(self.measure_type_list)
		measure_list_unique         = set(self.measure_list)
		additional_code_list_unique = set(self.additional_code_list)

		self.measure_count      = len(measure_list_unique)
		self.measure_type_count = len(measure_type_list_unique)
		self.additional_code_count = len(additional_code_list_unique)
		
		#print ("self.measure_count", self.measure_count)

		if self.measure_count == 1 and self.measure_type_count == 1 and self.additional_code_count == 1:
			for d in self.duty_list:
				self.combined_duty += d.duty_string + " "
		else:
			if self.measure_type_count > 1:
				#self.combined_duty = "More than one measure type"
				if "105" in measure_type_list_unique:
					for d in self.duty_list:
						if d.measure_type_id == "105":
							self.combined_duty += d.duty_string + " "
			elif self.additional_code_count > 1:
				#self.combined_duty = "More than one additional code"
				if "500" in additional_code_list_unique:
					for d in self.duty_list:
						if d.additional_code_id == "500":
							self.combined_duty += d.duty_string + " "
				if "550" in additional_code_list_unique:
					for d in self.duty_list:
						if d.additional_code_id == "550":
							self.combined_duty += d.duty_string + " "
	
		self.combined_duty = self.combined_duty.replace("  ", " ")
		self.combined_duty = self.combined_duty.strip()

class davidowen_commodity(object):
	def __init__(self, goods_nomenclature_item_id, duty_expression, end_date):
		self.duty_expression			= duty_expression
		self.goods_nomenclature_item_id	= goods_nomenclature_item_id
		self.end_date					= end_date
