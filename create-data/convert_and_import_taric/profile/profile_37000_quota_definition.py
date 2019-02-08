import psycopg2
import common.globals as g

class profile_37000_quota_definition(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                  = app.getDatestamp()
		quota_definition_sid			= app.getNumberValue(oMessage, ".//oub:quota.definition.sid", True)
		quota_order_number_id			= app.getValue(oMessage, ".//oub:quota.order.number.id", True)
		quota_order_number_sid			= app.getValue(oMessage, ".//oub:quota.order.number.sid", True)
		validity_start_date				= app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		validity_end_date				= app.getDateValue(oMessage, ".//oub:validity.end.date", True)
		volume					        = app.getValue(oMessage, ".//oub:volume", True)
		initial_volume					= app.getValue(oMessage, ".//oub:initial.volume", True)
		monetary_unit_code			    = app.getValue(oMessage, ".//oub:monetary.unit.code", True)
		measurement_unit_code			= app.getValue(oMessage, ".//oub:measurement.unit.code", True)
		measurement_unit_qualifier_code	= app.getValue(oMessage, ".//oub:measurement.unit.qualifier.code", True)
		maximum_precision	            = app.getValue(oMessage, ".//oub:maximum.precision", True)
		critical_state	                = app.getValue(oMessage, ".//oub:critical.state", True)
		critical_threshold          	= app.getValue(oMessage, ".//oub:critical.threshold", True)
		description	                    = app.getValue(oMessage, ".//oub:description", True)

		if update_type == "20":
			app.doprint ("Deleting quota definition " + str(quota_definition_sid))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM quota_definitions_oplog WHERE quota_definition_sid = %s", (quota_definition_sid,))
				app.conn.commit()
			except:
				g.app.log_error("quota definition", "D", quota_definition_sid, None, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":	# UPDATE
				operation = "U"
				app.doprint ("Updating quota definition " + str(quota_definition_sid))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting quota definition " + str(quota_definition_sid))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating quota definition " + str(quota_definition_sid))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO quota_definitions_oplog (quota_definition_sid, quota_order_number_id, validity_start_date,
				validity_end_date, volume, initial_volume, quota_order_number_sid,
				monetary_unit_code, measurement_unit_code, measurement_unit_qualifier_code,
				maximum_precision, critical_state, critical_threshold, description,
				operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
				(quota_definition_sid, quota_order_number_id, validity_start_date,
				validity_end_date, volume, initial_volume, quota_order_number_sid,
				monetary_unit_code, measurement_unit_code, measurement_unit_qualifier_code,
				maximum_precision, critical_state, critical_threshold, description,
				operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("quota definition", operation, quota_definition_sid, None, transaction_id, message_id)
			cur.close()
