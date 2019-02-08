import sys
import functions

class measure(object):
	def __init__(self, measure_type_description, measure_type_id, measure_sid, geographical_area_id, goods_nomenclature_item_id, sAdditionalCodeTypeID, additional_code_id, validity_start_date, validity_end_date, order_number, additional_code_description, geographical_area_description, regulation_id_full):
		# Get parameters from instantiator
		self.measure_type_description		= measure_type_description
		self.measure_type_id				= measure_type_id
		self.measure_sid					= measure_sid
		self.geographical_area_id			= geographical_area_id
		self.goods_nomenclature_item_id		= functions.mstr(goods_nomenclature_item_id)
		self.sAdditionalCodeTypeID			= sAdditionalCodeTypeID
		self.additional_code_id				= additional_code_id
		self.validity_start_date			= str(validity_start_date)
		self.validity_end_date				= str(validity_end_date)
		self.order_number					= order_number
		self.additional_code_description	= additional_code_description
		self.geographical_area_description	= geographical_area_description
		self.regulation_id_full				= regulation_id_full
		self.measure_type_full				= ""
		self.additional_code_full			= ""
		self.geographical_area_full			= ""
		self.validity_dates					= ""
		self.components                  = ""
		self.components_excel             = ""
		self.conditions                  = ""
		self.conditions_excel             = ""
		self.footnotes                   = ""

		self.delimiter                   = "|"
		self.delimiter_excel              = " "
		
		self.goods_description_lookup()
		self.concatenateFields()
		
	def goods_description_lookup(self):
		self.goods_description = ""
		for commodity in functions.app.commodity_list:
			a = functions.mstr(commodity.commodity_code[:6])
			b = functions.mstr(self.goods_nomenclature_item_id[:6])
			if a == b:
				self.goods_description = commodity.description[:100]
				break


	def concatenateFields(self):
		self.measure_type_full = "[" + str(self.measure_type_id) + "] " + str(self.measure_type_description)
		if str(self.sAdditionalCodeTypeID) == "None":
			self.additional_code_full = ""
		else:
			self.additional_code_full = "[" + str(self.sAdditionalCodeTypeID) + str(self.additional_code_id) + "] " + str(self.additional_code_description)
		self.geographical_area_full = "[" + str(self.geographical_area_id) + "] " + str(self.geographical_area_description)
		
		if self.validity_start_date != "None":
			#self.validity_dates = self.validity_start_date
			self.validity_dates = functions.fmtDate2(self.validity_start_date)
			if self.validity_end_date != "None":
				self.validity_dates += " - " + functions.fmtDate2(self.validity_end_date)
			else:
				self.validity_dates += " - no end date"

	def addComponents(self, lstMeasureComponents):
		for mc in lstMeasureComponents:
			if mc.measure_sid == self.measure_sid:
				self.components += mc.duty_string
				self.components += " " + self.delimiter + " "

		self.components = self.components.strip()
		self.components = self.components.strip(self.delimiter)
		self.components = self.components.strip()
		
		self.components_excel = self.components.replace(" " + self.delimiter + " ", self.delimiter_excel)

	def addFootnotes(self, lstFootnotes):
		for f in lstFootnotes:
			if f.measure_sid == self.measure_sid:
				self.footnotes += f.sFootnoteFull
				self.footnotes += " " + self.delimiter + " "
		self.footnotes = self.footnotes.strip()
		self.footnotes = self.footnotes.strip(self.delimiter)
		self.footnotes = self.footnotes.strip()

		self.components_excel = self.components.replace(" " + self.delimiter + " ", self.delimiter_excel)

	def addConditions(self, lstConditions):
		i = 1
		for c in lstConditions:
			if c.measure_sid == self.measure_sid:
				self.conditions += c.sConditionFull.replace("#", str(i))
				self.conditions += self.delimiter + self.delimiter
				i = i + 1
		self.conditions = self.conditions.strip()
		self.conditions = self.conditions.strip(self.delimiter)
		self.conditions = self.conditions.strip()

		self.conditions_excel = self.conditions.replace(" " + self.delimiter + " ", "\n")
		self.conditions_excel = self.conditions_excel.replace(self.delimiter, "\n")
		self.conditions_excel = self.conditions_excel.replace(" : " , "\n")
		self.conditions_excel = self.conditions_excel.replace("\n\n" , "\n")
