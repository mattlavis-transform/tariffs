import psycopg2
from datetime import datetime
import common.globals as g

class profile_44000_monetary_exchange_period(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                      = app.getDatestamp()
		monetary_exchange_period_sid	    = app.getNumberValue(oMessage, ".//oub:monetary.exchange.period.sid", True)
		parent_monetary_unit_code			= app.getValue(oMessage, ".//oub:parent.monetary.unit.code", True)
		validity_start_date					= app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		validity_end_date					= app.getDateValue(oMessage, ".//oub:validity.end.date", True)

		if update_type == "20":
			app.doprint ("Deleting monetary exchange period " + str(monetary_exchange_period_sid))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM monetary_exchange_periods_oplog WHERE monetary_exchange_period_sid = %s", (monetary_exchange_period_sid,))
				app.conn.commit()
			except:
				g.app.log_error("monetary exchange period", "D", monetary_exchange_period_sid, None, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":	# Update
				operation = "U"
				app.doprint ("Updating monetary exchange period " + str(monetary_exchange_period_sid))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting monetary exchange period " + str(monetary_exchange_period_sid))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating monetary exchange period " + str(monetary_exchange_period_sid))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO monetary_exchange_periods_oplog (monetary_exchange_period_sid,
				parent_monetary_unit_code, validity_start_date, validity_end_date,
				operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s)""", 
				(monetary_exchange_period_sid,
				parent_monetary_unit_code, validity_start_date, validity_end_date,
				operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("monetary exchange period", operation, monetary_exchange_period_sid, None, transaction_id, message_id)
			cur.close()
