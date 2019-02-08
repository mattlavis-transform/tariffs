import psycopg2
import common.globals as g

class profile_12005_additional_code_type_description(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                  = app.getDatestamp()
		additional_code_type_id			= app.getValue(oMessage, ".//oub:additional.code.type.id", True)
		language_id						= app.getValue(oMessage, ".//oub:language.id", True)
		description						= app.getValue(oMessage, ".//oub:description", True)

		if update_type == "20":
			app.doprint ("Deleting additional code type description " + str(additional_code_type_id))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM additional_code_type_descriptions_oplog WHERE additional_code_type_id = %s", (additional_code_type_id,))
				app.conn.commit()
			except:
				g.app.log_error("additional_code_type_description", "D", None, additional_code_type_id, transaction_id, message_id)

			cur.close()

		else:
			if update_type == "1":	# UPDATE
				operation = "U"
				app.doprint ("Updating additional code type description " + str(additional_code_type_id))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting additional code type description " + str(additional_code_type_id))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating additional code type description " + str(additional_code_type_id))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO additional_code_type_descriptions_oplog (additional_code_type_id, language_id,
				description, operation, operation_date)
				VALUES (%s, %s, %s, %s, %s)""", 
				(additional_code_type_id, language_id,
				description, operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("additional_code_type_description", operation, None, additional_code_type_id, transaction_id, message_id)
			cur.close()
