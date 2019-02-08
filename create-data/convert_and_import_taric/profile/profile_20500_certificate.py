import psycopg2
import common.globals as g

class profile_20500_certificate(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                      = app.getDatestamp()
		certificate_type_code				= app.getValue(oMessage, ".//oub:certificate.type.code", True)
		certificate_code					= app.getValue(oMessage, ".//oub:certificate.code", True)
		validity_start_date					= app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		validity_end_date					= app.getDateValue(oMessage, ".//oub:validity.end.date", True)

		if update_type == "20":
			app.doprint ("Deleting certificate " + str(certificate_code))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM certificates_oplog WHERE certificate_type_code = %s AND certificate_code = %s", (certificate_type_code, certificate_code,))
				app.conn.commit()
			except:
				g.app.log_error("certificate", "D", None, certificate_type_code + "|" + certificate_code, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":	# UPDATE
				operation = "U"
				app.doprint ("Updating certificate " + str(certificate_code))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting certificate " + str(certificate_code))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating certificate " + str(certificate_code))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO certificates_oplog (certificate_type_code, certificate_code,
				validity_start_date, validity_end_date, operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s)""", 
				(certificate_type_code, certificate_code, validity_start_date, validity_end_date, operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("certificate", operation, None, certificate_type_code + "|" + certificate_code, transaction_id, message_id)
			cur.close()
