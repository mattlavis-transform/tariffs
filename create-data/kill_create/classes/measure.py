import classes.functions as f
import classes.globals as g
import datetime
from datetime import datetime
import sys

from classes.measure_component import measure_component


class measure(object):
	def __init__(self, measure_sid, ordernumber, measure_type_id, validity_start_date, validity_end_date,
		geographical_area_id, goods_nomenclature_item_id, additional_code_type_id, additional_code_id,
		reduction_indicator, measure_generating_regulation_role,
		measure_generating_regulation_id, justification_regulation_role, justification_regulation_id,
		stopped_flag, geographical_area_sid, goods_nomenclature_sid,
		additional_code_sid, export_refund_nomenclature_sid):
		# from parameters
		self.measure_sid  			    		= measure_sid
		self.quota_order_number_id    			= ordernumber
		self.measure_type_id      				= measure_type_id
		self.validity_start_date				= validity_start_date
		self.validity_end_date      			= validity_end_date
		self.geographical_area_id     			= geographical_area_id
		self.goods_nomenclature_item_id 		= goods_nomenclature_item_id
		self.additional_code_type_id			= additional_code_type_id
		self.additional_code_id					= additional_code_id
		self.reduction_indicator				= reduction_indicator
		self.measure_generating_regulation_role	= measure_generating_regulation_role
		self.measure_generating_regulation_id	= measure_generating_regulation_id
		self.justification_regulation_role		= justification_regulation_role
		self.justification_regulation_id		= justification_regulation_id
		self.stopped_flag						= stopped_flag
		self.geographical_area_sid				= geographical_area_sid
		self.goods_nomenclature_sid				= goods_nomenclature_sid
		self.additional_code_sid				= additional_code_sid
		self.export_refund_nomenclature_sid		= export_refund_nomenclature_sid

		# Initialised
		self.measure_component_list						= []
		self.measure_condition_list						= []
		self.measure_condition_component_list			= []
		self.measure_excluded_geographical_area_list	= []
		self.measure_footnote_list						= []
		self.measure_partial_temporary_stop_list		= []
		
		# Derived
		self.validity_start_year	= self.validity_start_date.year
		self.validity_start_month	= self.validity_start_date.month
		self.validity_start_day		= self.validity_start_date.day

		if self.validity_end_date != None:
			self.validity_end_year		= self.validity_end_date.year
			self.validity_end_month		= self.validity_end_date.month
			self.validity_end_day		= self.validity_end_date.day
			self.period_length			= (self.validity_end_date - self.validity_start_date).days + 1

	def append_component(self, duty_expression_id, duty_amount, monetary_unit, measurement_unit_code, measurement_unit_qualifier_code):
		mc = measure_component(self.measure_sid, duty_expression_id, duty_amount, monetary_unit, measurement_unit_code, measurement_unit_qualifier_code)
		self.measure_component_list.append(mc)



	def xml(self):
		app = g.app
		s = app.template_measure
		s = s.replace("[TRANSACTION_ID]",         			str(app.transaction_id))
		s = s.replace("[MESSAGE_ID]",             			str(app.sequence_id))
		s = s.replace("[RECORD_SEQUENCE_NUMBER]", 			str(app.sequence_id))

		for obj in self.measure_component_list:
			obj.update_type = "3"
			obj.measure_sid = self.measure_sid

		# Get the update type
		s = s.replace("[UPDATE_TYPE]",						  "3") # This is a restart, therefore an insert [3]
		s = s.replace("[MEASURE_SID]",                        f.mstr(self.measure_sid))
		s = s.replace("[MEASURE_TYPE_ID]",                    f.mstr(self.measure_type_id))
		s = s.replace("[GEOGRAPHICAL_AREA_ID]",               f.mstr(self.geographical_area_id))
		s = s.replace("[GOODS_NOMENCLATURE_ITEM_ID]",         f.mstr(self.goods_nomenclature_item_id))
		s = s.replace("[MEASURE_GENERATING_REGULATION_ROLE]", f.mstr(self.measure_generating_regulation_role))
		s = s.replace("[MEASURE_GENERATING_REGULATION_ID]",   f.mstr(self.measure_generating_regulation_id))
		s = s.replace("[JUSTIFICATION_REGULATION_ROLE]",      f.mstr(self.justification_regulation_role))
		s = s.replace("[JUSTIFICATION_REGULATION_ID]",        f.mstr(self.justification_regulation_id))
		s = s.replace("[STOPPED_FLAG]",                       f.mstr(self.stopped_flag))
		s = s.replace("[GEOGRAPHICAL_AREA_SID]",              f.mstr(self.geographical_area_sid))
		s = s.replace("[GOODS_NOMENCLATURE_SID]",             f.mstr(self.goods_nomenclature_sid))
		s = s.replace("[ORDERNUMBER]",                        f.mstr(self.quota_order_number_id))
		s = s.replace("[ADDITIONAL_CODE_TYPE_ID]",            f.mstr(self.additional_code_type_id))
		s = s.replace("[ADDITIONAL_CODE_ID]",                 f.mstr(self.additional_code_id))
		s = s.replace("[ADDITIONAL_CODE_SID]",                f.mstr(self.additional_code_sid))
		s = s.replace("[REDUCTION_INDICATOR]",                f.mstr(self.reduction_indicator))
		s = s.replace("[EXPORT_REFUND_NOMENCLATURE_SID]",     f.mstr(self.export_refund_nomenclature_sid))
		s = s.replace("[VALIDITY_START_DATE]",     			  f.mdate(self.validity_start_date))
		s = s.replace("[VALIDITY_END_DATE]",     			  f.mdate(self.validity_end_date))

		s = s.replace("\t\t\t\t\t\t<oub:validity.end.date></oub:validity.end.date>\n", "")
		s = s.replace("\t\t\t\t\t\t<oub:goods.nomenclature.item.id></oub:goods.nomenclature.item.id>\n", "")
		s = s.replace("\t\t\t\t\t\t<oub:additional.code.type></oub:additional.code.type>\n", "")
		s = s.replace("\t\t\t\t\t\t<oub:additional.code></oub:additional.code>\n", "")
		s = s.replace("\t\t\t\t\t\t<oub:ordernumber></oub:ordernumber>\n", "")
		s = s.replace("\t\t\t\t\t\t<oub:reduction.indicator></oub:reduction.indicator>\n", "")
		s = s.replace("\t\t\t\t\t\t<oub:justification.regulation.role></oub:justification.regulation.role>\n", "")
		s = s.replace("\t\t\t\t\t\t<oub:justification.regulation.id></oub:justification.regulation.id>\n", "")
		s = s.replace("\t\t\t\t\t\t<oub:geographical.area.sid></oub:geographical.area.sid>\n", "")
		s = s.replace("\t\t\t\t\t\t<oub:goods.nomenclature.sid></oub:goods.nomenclature.sid>\n", "")
		s = s.replace("\t\t\t\t\t\t<oub:additional.code.sid></oub:additional.code.sid>\n", "")
		s = s.replace("\t\t\t\t\t\t<oub:export.refund.nomenclature.sid></oub:export.refund.nomenclature.sid>\n", "")

		app.sequence_id += 1
		
		self.component_content = ""
		self.condition_content = ""
		self.condition_component_content = ""
		self.exclusion_content = ""
		self.footnote_content = ""
		self.pts_content = ""

		# The code below is executed when we are converting MFNs, i.e. the duty type is 103s and 105s

		for obj in self.measure_component_list:
			self.component_content += obj.xml(self.measure_type_id, self.goods_nomenclature_item_id)

		for obj in self.measure_condition_list:
			self.condition_content += obj.xml()

		for obj in self.measure_condition_component_list:
			self.condition_component_content += obj.xml()

		for obj in self.measure_excluded_geographical_area_list:
			self.exclusion_content += obj.xml()

		for obj in self.measure_footnote_list:
			self.footnote_content += obj.xml()

		for obj in self.measure_partial_temporary_stop_list:
			self.pts_content += obj.xml()

		s = s.replace("[COMPONENTS]\n", 			self.component_content)
		s = s.replace("[CONDITIONS]\n", 			self.condition_content)
		s = s.replace("[CONDITION_COMPONENTS]\n",	self.condition_component_content)
		s = s.replace("[EXCLUDED]\n", 				self.exclusion_content)
		s = s.replace("[FOOTNOTES]\n", 				self.footnote_content)
		s = s.replace("[PTS]\n",	 				self.pts_content)

		g.app.transaction_id += 1
		return (s)