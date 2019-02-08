import psycopg2
import common.globals as g

class profile_11005_certificate_type_description(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                  = app.getDatestamp()
		certificate_type_code			= app.getValue(oMessage, ".//oub:certificate.type.code", True)
		language_id						= app.getValue(oMessage, ".//oub:language.id", True)
		description						= app.getValue(oMessage, ".//oub:description", True)

		if update_type == "20":
			app.doprint ("Deleting certificate type description " + str(certificate_type_code))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM certificate_type_descriptions_oplog WHERE certificate_type_code = %s", (certificate_type_code,))
				app.conn.commit()
			except:
				g.app.log_error("certificate_type_description", "D", None, certificate_type_code, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":		# UPDATE
				operation = "U"
				app.doprint ("Updating certificate type description " + str(certificate_type_code))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting certificate type description " + str(certificate_type_code))
			else:						# INSERT
				operation = "C"
				app.doprint ("Creating certificate type description " + str(certificate_type_code))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO certificate_type_descriptions_oplog (certificate_type_code, language_id,
				description, operation, operation_date)
				VALUES (%s, %s, %s, %s, %s)""", 
				(certificate_type_code, language_id,
				description, operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("certificate_type_description", operation, None, certificate_type_code, transaction_id, message_id)
			cur.close()
