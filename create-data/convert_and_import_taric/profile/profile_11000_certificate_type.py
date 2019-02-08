import psycopg2
import common.globals as g

class profile_11000_certificate_type(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                      = app.getDatestamp()
		certificate_type_code				= app.getValue(oMessage, ".//oub:certificate.type.code", True)
		validity_start_date					= app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		validity_end_date					= app.getDateValue(oMessage, ".//oub:validity.end.date", True)

		if update_type == "20":
			app.doprint ("Deleting certificate type " + str(certificate_type_code))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM measures_oplog WHERE certificate_type_code = %s", (certificate_type_code,))
				app.conn.commit()
			except:
				g.app.log_error("certificate_type", "D", None, certificate_type_code, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":	# Update
				operation = "U"
				app.doprint ("Updating certificate type " + str(certificate_type_code))
			elif update_type == "2":	# Update
				operation = "D"
				app.doprint ("Deleting certificate type " + str(certificate_type_code))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating certificate type " + str(certificate_type_code))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO certificate_types_oplog (certificate_type_code, validity_start_date,
				validity_end_date, operation, operation_date)
				VALUES (%s, %s, %s, %s, %s)""", 
				(certificate_type_code, validity_start_date,
				validity_end_date, operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("certificate_type", operation, None, certificate_type_code, transaction_id, message_id)
			cur.close()
