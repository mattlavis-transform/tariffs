import psycopg2
import common.globals as g

class profile_43005_measure_component(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                  = app.getDatestamp()
		measure_sid						= app.getNumberValue(oMessage, ".//oub:measure.sid", True)
		duty_expression_id				= app.getValue(oMessage, ".//oub:duty.expression.id", True)
		duty_amount					    = app.getValue(oMessage, ".//oub:duty.amount", True)
		monetary_unit_code			    = app.getValue(oMessage, ".//oub:monetary.unit.code", True)
		measurement_unit_code			= app.getValue(oMessage, ".//oub:measurement.unit.code", True)
		measurement_unit_qualifier_code	= app.getValue(oMessage, ".//oub:measurement.unit.qualifier.code", True)

		if update_type == "20":
			app.doprint ("Deleting measure component " + str(measure_sid))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM measure_components_oplog WHERE measure_sid = %s AND duty_expression_id = %s", (measure_sid, duty_expression_id,))
				app.conn.commit()
			except:
				g.app.log_error("measure component", "D", measure_sid, None, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":	# Update
				operation = "U"
				app.doprint ("Updating measure component on measure_sid " + str(measure_sid))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting measure component on measure_sid " + str(measure_sid))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating measure component on measure_sid " + str(measure_sid))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO measure_components_oplog (measure_sid, duty_expression_id, duty_amount,
				monetary_unit_code, measurement_unit_code,
				measurement_unit_qualifier_code, operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
				(measure_sid, duty_expression_id, duty_amount,
				monetary_unit_code, measurement_unit_code,
				measurement_unit_qualifier_code, operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("measure component", operation, measure_sid, None, transaction_id, message_id)
			cur.close()
