import functions

class condition(object):
	def __init__(self, measure_sid, measure_condition_sid, condition_code, condition_code_description, action_code, measure_action_code, condition_duty_amount, certificate_type_code, certificate_type_code_description, certificate_code, certificate_description, monetary_unit_code, measurement_unit_code, measurement_unit_qualifier_code, measurement_unit_code_description, measurement_unit_qualifier_codeDescription):
		
		# Get parameters from instantiator
		self.measure_sid								= measure_sid
		self.measure_condition_sid						= measure_condition_sid
		self.condition_code								= condition_code
		self.condition_code_description					= condition_code_description
		self.action_code								= action_code
		self.measure_action_code						= measure_action_code
		self.condition_duty_amount						= condition_duty_amount
		self.certificate_type_code						= certificate_type_code
		self.certificate_type_code_description			= certificate_type_code_description
		self.certificate_code							= certificate_code
		self.certificate_description					= certificate_description
		self.monetary_unit_code							= monetary_unit_code
		self.measurement_unit_code						= measurement_unit_code
		self.measurement_unit_qualifier_code            = measurement_unit_qualifier_code
		self.measurement_unit_code_description          = measurement_unit_code_description
		self.measurement_unit_qualifier_codeDescription = measurement_unit_qualifier_codeDescription

		if self.condition_code == "V":
			if not(self.measure_sid in functions.app.siv_measure_sid_list):
				functions.app.siv_count += 1

		functions.app.siv_measure_sid_list.add (self.measure_sid)
		functions.app.condition_count += 1

		self.sMUQ = ""
		self.sConditionFull = ""
		self.concatenateFields()
		
	def concatenateFields(self):
		if self.measurement_unit_qualifier_code == None or self.measurement_unit_qualifier_codeDescription == None:
			self.sMUQ = ""
		else:
			self.sMUQ = self.measurement_unit_qualifier_code + self.measurement_unit_qualifier_codeDescription
			
		self.sConditionFull = ""
		# Condition statement
		self.sConditionFull += "Condition [" + self.condition_code + "#] " + self.condition_code_description + " : "
		# Document statement
		if self.certificate_code != None:
			self.sConditionFull += "Document [" + self.certificate_type_code + "] "		
		# Action statement
		if self.action_code != None:
			self.sConditionFull += "Action [" + self.action_code + "] " + self.measure_action_code + " : "
		# Requirement statement
		if self.condition_duty_amount != None:
			self.sConditionFull += "Requirement - " + "{:.2f}".format(self.condition_duty_amount)
			if self.measurement_unit_code_description != None:
				self.sConditionFull += " " + self.measurement_unit_code_description
				if self.measurement_unit_qualifier_codeDescription != None:
					self.sConditionFull += " " + self.measurement_unit_qualifier_codeDescription
			
