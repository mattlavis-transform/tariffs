import psycopg2
import common.globals as g

class profile_20505_certificate_description_period(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date				        = app.getDatestamp()
		certificate_description_period_sid  = app.getNumberValue(oMessage, ".//oub:certificate.description.period.sid", True)
		certificate_type_code			    = app.getValue(oMessage, ".//oub:certificate.type.code", True)
		certificate_code				    = app.getValue(oMessage, ".//oub:certificate.code", True)
		validity_start_date			        = app.getDateValue(oMessage, ".//oub:validity.start.date", True)

		if update_type == "20":
			app.doprint ("Deleting certificate description period " + str(certificate_description_period_sid))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM certificate_description_periods_oplog WHERE certificate_description_period_sid = %s", (certificate_description_period_sid,))
				app.conn.commit()
			except:
				g.app.log_error("certificate description period", "D", certificate_description_period_sid, certificate_type_code + "|" + certificate_code, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":	# Update
				operation = "U"
				app.doprint ("Updating certificate description period " + str(certificate_description_period_sid))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting certificate description period " + str(certificate_description_period_sid))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating certificate description period " + str(certificate_description_period_sid))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO certificate_description_periods_oplog (certificate_description_period_sid,
				certificate_type_code, certificate_code, validity_start_date, operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s)""", 
				(certificate_description_period_sid, certificate_type_code, certificate_code, validity_start_date, operation, operation_date))
			except:
				g.app.log_error("certificate description period", operation, certificate_description_period_sid, certificate_type_code + "|" + certificate_code, transaction_id, message_id)
			app.conn.commit()
			cur.close()
