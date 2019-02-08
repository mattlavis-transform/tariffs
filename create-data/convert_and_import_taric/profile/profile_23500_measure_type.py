import psycopg2
import sys
import common.globals as g

class profile_23500_measure_type(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                      = app.getDatestamp()
		measure_type_id						= app.getValue(oMessage, ".//oub:measure.type.id", True)
		validity_start_date					= app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		validity_end_date					= app.getDateValue(oMessage, ".//oub:validity.end.date", True)
		trade_movement_code					= app.getValue(oMessage, ".//oub:trade.movement.code", True)
		priority_code						= app.getValue(oMessage, ".//oub:priority.code", True)
		measure_component_applicable_code	= app.getValue(oMessage, ".//oub:measure.component.applicable.code", True)
		origin_dest_code					= app.getValue(oMessage, ".//oub:origin.dest.code", True)
		order_number_capture_code			= app.getValue(oMessage, ".//oub:order.number.capture.code", True)
		measure_explosion_level				= app.getValue(oMessage, ".//oub:measure.explosion.level", True)
		measure_type_series_id				= app.getValue(oMessage, ".//oub:measure.type.series.id", True)

		if update_type == "20":
			app.doprint ("Deleting measure type " + str(measure_type_id))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM measure_types_oplog WHERE measure_type_id = %s", (measure_type_id,))
				app.conn.commit()
			except:
				g.app.log_error("measure type", "D", None, measure_type_id, transaction_id, message_id)
			cur.close()

		else:
			if not(measure_type_id.isnumeric()):
				national = True
			else:
				national = None
			if update_type == "1":	# Update
				operation = "U"
				app.doprint ("Updating measure type " + str(measure_type_id))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting measure type " + str(measure_type_id))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating measure type " + str(measure_type_id))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO measure_types_oplog (measure_type_id, validity_start_date, validity_end_date,
				trade_movement_code, priority_code, measure_component_applicable_code,
				origin_dest_code, order_number_capture_code, measure_explosion_level, 
				measure_type_series_id, operation, operation_date, national)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
				(measure_type_id, validity_start_date, validity_end_date,
				trade_movement_code, priority_code, measure_component_applicable_code,
				origin_dest_code, order_number_capture_code, measure_explosion_level, 
				measure_type_series_id, operation, operation_date, national))
				app.conn.commit()
			except:
				g.app.log_error("measure type", operation, None, measure_type_id, transaction_id, message_id)
			cur.close()
