import psycopg2
import common.globals as g

class profile_24510_additional_code_description(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                          = app.getDatestamp()
		additional_code_description_period_sid	= app.getNumberValue(oMessage, ".//oub:additional.code.description.period.sid", True)
		additional_code_sid	                    = app.getNumberValue(oMessage, ".//oub:additional.code.sid", True)
		additional_code_type_id		            = app.getValue(oMessage, ".//oub:additional.code.type.id", True)
		additional_code			    			= app.getValue(oMessage, ".//oub:additional.code", True)
		language_id								= app.getValue(oMessage, ".//oub:language.id", True)
		description								= app.getValue(oMessage, ".//oub:description", True)

		if update_type == "20":
			app.doprint ("Deleting additional code description " + str(additional_code_description_period_sid))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM additional_code_descriptions_oplog WHERE additional_code_description_period_sid = %s", (additional_code_description_period_sid,))
				app.conn.commit()
			except:
				g.app.log_error("additional code description", "D", additional_code_description_period_sid, additional_code_type_id + "|" + additional_code, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":		# UPDATE
				operation = "U"
				app.doprint ("Updating additional code type description " + str(additional_code_description_period_sid))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting additional code type description " + str(additional_code_description_period_sid))
			else:						# INSERT
				operation = "C"
				app.doprint ("Creating additional code type description " + str(additional_code_description_period_sid))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO additional_code_descriptions_oplog (additional_code_description_period_sid,
				additional_code_sid, additional_code_type_id,
				additional_code, language_id, description, operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
				(additional_code_description_period_sid, additional_code_sid, additional_code_type_id,
				additional_code, language_id, description, operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("additional code description", operation, additional_code_description_period_sid, additional_code_type_id + "|" + additional_code, transaction_id, message_id)
			cur.close()
