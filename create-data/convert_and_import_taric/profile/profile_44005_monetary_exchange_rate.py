import psycopg2
from datetime import datetime
import common.globals as g

class profile_44005_monetary_exchange_rate(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                  = app.getDatestamp()
		monetary_exchange_period_sid	= app.getNumberValue(oMessage, ".//oub:monetary.exchange.period.sid", True)
		child_monetary_unit_code		= app.getValue(oMessage, ".//oub:child.monetary.unit.code", True)
		exchange_rate					= app.getDateValue(oMessage, ".//oub:exchange.rate", True)

		if update_type == "20":
			app.doprint ("Deleting monetary exchange rate " + str(monetary_exchange_period_sid))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM monetary_exchange_rates_oplog WHERE monetary_exchange_period_sid = %s", (monetary_exchange_period_sid,))
				app.conn.commit()
			except:
				g.app.log_error("monetary exchange rate", "D", monetary_exchange_period_sid, None, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":	# Update
				operation = "U"
				app.doprint ("Updating monetary exchange rate " + str(monetary_exchange_period_sid))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting monetary exchange rate " + str(monetary_exchange_period_sid))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating monetary exchange rate " + str(monetary_exchange_period_sid))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO monetary_exchange_rates_oplog (monetary_exchange_period_sid,
				child_monetary_unit_code, exchange_rate,
				operation, operation_date)
				VALUES (%s, %s, %s, %s, %s)""", 
				(monetary_exchange_period_sid,
				child_monetary_unit_code, exchange_rate,
				operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("monetary exchange rate", operation, monetary_exchange_period_sid, None, transaction_id, message_id)
			cur.close()
