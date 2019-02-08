import psycopg2
import common.globals as g

class profile_12000_additional_code_type(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                      = app.getDatestamp()
		additional_code_type_id				= app.getValue(oMessage, ".//oub:additional.code.type.id", True)
		validity_start_date					= app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		validity_end_date					= app.getDateValue(oMessage, ".//oub:validity.end.date", True)
		application_code					= app.getValue(oMessage, ".//oub:application.code", True)
		meursing_table_plan_id				= app.getValue(oMessage, ".//oub:meursing.table.plan.id", True)

		if update_type == "20":
			app.doprint ("Deleting additional code type " + str(additional_code_type_id))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM additional_code_types_oplog WHERE additional_code_type_id = %s", (additional_code_type_id,))
				app.conn.commit()
			except:
				g.app.log_error("additional_code_type", "D", None, additional_code_type_id, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":		# UPDATE
				operation = "U"
				app.doprint ("Updating additional code type " + str(additional_code_type_id))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting additional code type " + str(additional_code_type_id))
			else:						# INSERT
				operation = "C"
				app.doprint ("Creating additional code type " + str(additional_code_type_id))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO additional_code_types_oplog (additional_code_type_id, validity_start_date,
				validity_end_date, application_code, meursing_table_plan_id, operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
				(additional_code_type_id, validity_start_date,
				validity_end_date, application_code, meursing_table_plan_id, operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("additional_code_type", operation, None, additional_code_type_id, transaction_id, message_id)
			cur.close()
