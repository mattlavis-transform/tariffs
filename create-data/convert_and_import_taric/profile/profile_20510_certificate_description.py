import psycopg2
import common.globals as g

class profile_20510_certificate_description(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                  	= app.getDatestamp()
		certificate_description_period_sid  = app.getNumberValue(oMessage, ".//oub:certificate.description.period.sid", True)
		language_id							= app.getValue(oMessage, ".//oub:language.id", True)
		certificate_type_code				= app.getValue(oMessage, ".//oub:certificate.type.code", True)
		certificate_code					= app.getValue(oMessage, ".//oub:certificate.code", True)
		description							= app.getValue(oMessage, ".//oub:description", True)

		if update_type == "20":
			app.doprint ("Deleting certificate description " + str(certificate_description_period_sid))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM certificate_descriptions_oplog WHERE certificate_description_period_sid = %s", (certificate_description_period_sid,))
				app.conn.commit()
			except:
				g.app.log_error("certificate description", "D", certificate_description_period_sid, certificate_type_code + "|" + certificate_code, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":		# UPDATE
				operation = "U"
				app.doprint ("Updating certificate description " + str(certificate_description_period_sid))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting certificate description " + str(certificate_description_period_sid))
			else:						# INSERT
				operation = "C"
				app.doprint ("Creating certificate description " + str(certificate_description_period_sid))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO certificate_descriptions_oplog (certificate_description_period_sid, language_id,
				certificate_type_code, certificate_code, description, operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
				(certificate_description_period_sid, language_id,
				certificate_type_code, certificate_code, description, operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("certificate description", operation, certificate_description_period_sid, certificate_type_code + "|" + certificate_code, transaction_id, message_id)
			cur.close()
