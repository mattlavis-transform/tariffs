import re
import sys
from datetime import datetime

import classes.functions as fn
import classes.globals as g
from classes.measure import measure
from classes.measure_component import measure_component

class commodity(object):
	def __init__(self, goods_nomenclature_sid, goods_nomenclature_item_id, productline_suffix, number_indents, leaf, description):
		# Get parameters from instantiator
		self.goods_nomenclature_sid = goods_nomenclature_sid
		self.goods_nomenclature_item_id = goods_nomenclature_item_id
		self.productline_suffix         = productline_suffix
		self.number_indents             = number_indents
		self.leaf                       = leaf
		self.description                = description
		self.measure_list				= []
		self.all_children				= []
		self.leaf_children				= []

		# Get the necessary parameters
		measure_sid							= self.get_next_measure_sid()
		ordernumber							= ""
		measure_type_id						= self.get_measure_type_id()
		validity_start_date					= datetime.strptime("2019-03-30", "%Y-%m-%d")
		validity_end_date					= None
		geographical_area_id				= "1011"
		geographical_area_sid				= self.get_geographical_area_sid(geographical_area_id)
		additional_code_type_id				= None
		additional_code_id					= None
		reduction_indicator					= None
		measure_generating_regulation_role	= "1"
		measure_generating_regulation_id	= "M1900010"
		justification_regulation_role		= None
		justification_regulation_id			= None
		stopped_flag						= 0
		additional_code_sid					= None
		export_refund_nomenclature_sid		= None


		# Create a single measure component for each of these measures
		my_component = measure_component(measure_sid, "01", 0, "", "", "", self.goods_nomenclature_item_id)


		# Create a new measure for each commodity code
		my_measure = measure(measure_sid, ordernumber, measure_type_id, validity_start_date, validity_end_date,
		geographical_area_id, goods_nomenclature_item_id, additional_code_type_id, additional_code_id,
		reduction_indicator, measure_generating_regulation_role,
		measure_generating_regulation_id, justification_regulation_role, justification_regulation_id,
		stopped_flag, geographical_area_sid, goods_nomenclature_sid,
		additional_code_sid, export_refund_nomenclature_sid)

		my_measure.measure_component_list.append (my_component)
		self.measure_list.append(my_measure)

	def get_hierarchy(self, commodity_list):
		self.leaf_children = []
		for loop1 in range(0, len(commodity_list)):
			my_commodity = commodity_list[loop1]
			if (my_commodity.goods_nomenclature_item_id == self.goods_nomenclature_item_id) and (my_commodity.productline_suffix == "80"):
				for loop2 in range(loop1 + 1, len(commodity_list)):
					looped_commodity = commodity_list[loop2]
					if looped_commodity.number_indents > my_commodity.number_indents:
						self.all_children.append (looped_commodity)
						if looped_commodity.leaf == "1":
							self.leaf_children.append (looped_commodity)
					else:
						break
					



	def drop_zero_component(self):
		if len(self.measure_list) > 0:
			m = self.measure_list[0]
			if len(m.measure_component_list) > 0:
				if m.measure_component_list[0].duty_amount == 0:
					del m.measure_component_list[0]


	def append_component(self, duty_expression_id, duty_amount, monetary_unit, measurement_unit_code, measurement_unit_qualifier_code):
		if len(self.measure_list) > 0:
			m = self.measure_list[0]
			m.append_component(duty_expression_id, duty_amount, monetary_unit, measurement_unit_code, measurement_unit_qualifier_code)



	def get_next_measure_sid(self):
		g.app.last_measure_sid += 1

		measure_sid = g.app.last_measure_sid
		return (measure_sid)


	def get_measure_type_id(self):
		measure_type_id = "103"
		for item in g.app.authorised_use_list:
			if self.goods_nomenclature_item_id == item:
				measure_type_id = "105"
				break

		return (measure_type_id)


	def safe_get_measure_type_id(self):
		auth_use_array = []
		auth_use_array.append("for the manufacture")
		auth_use_array.append("industrial manufacture")
		auth_use_array.append("used for")
		auth_use_array.append("for use in")
		auth_use_array.append("for use on")
		auth_use_array.append("intended to be fitted")
		auth_use_array.append("for technical or industrial uses")
		auth_use_array.append("for industrial processing")
		auth_use_array.append("for industrial uses")
		auth_use_array.append("for the industrial")
		auth_use_array.append("for civil use")
		auth_use_array.append("for undergoing chemical transformation")
		auth_use_array.append("for processing")
		auth_use_array.append("for other purposes")
		auth_use_array.append("for the production of")
		auth_use_array.append("for undergoing")
		auth_use_array.append("for slaughter")
		auth_use_array.append("of apparatus of subheading")
		auth_use_array.append("in the manufacture of")
		auth_use_array.append("for seagoing vessels")
		auth_use_array.append("for refining")
		auth_use_array.append("for uses other than")
		auth_use_array.append("for use as a")
		auth_use_array.append("vessels and other floating structures for breaking up")

		measure_type_id = "103"
		for my_string in auth_use_array:
			s = self.description.lower()
			if s.find(my_string) > 0:
				measure_type_id = "105"
				break

		return (measure_type_id)



	def get_geographical_area_sid(self, geographical_area_id):
		if geographical_area_id == "1011":
			geographical_area_sid = 400
		return geographical_area_sid
	
	def get_mfn(self):
		pass


	def xml(self):
		my_xml = ""
		for m in self.measure_list:
			my_xml += m.xml()

		return (my_xml)