import psycopg2
import sys
from datetime import datetime
import common.globals as g

class profile_10000_footnote_type(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date		= app.getDatestamp()
		footnote_type_id	= app.getValue(oMessage, ".//oub:footnote.type.id", True)
		validity_start_date	= app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		validity_end_date	= app.getDateValue(oMessage, ".//oub:validity.end.date", True)
		application_code	= app.getValue(oMessage, ".//oub:application.code", True)

		if update_type == "20":
			cur = app.conn.cursor()
			app.doprint ("Deleting footnote type " + str(footnote_type_id))
			try:
				cur.execute("DELETE FROM footnote_types_oplog WHERE footnote_type_id = %s", (footnote_type_id,))
				app.conn.commit()
			except:
				g.app.log_error("footnote_type", "D", None, footnote_type_id, transaction_id, message_id)
			cur.close()

		else:
			if footnote_type_id in ('01', '02', '03', '05', '05', '06'):
				national = True
			else:
				national = None
			if update_type == "1":	# UPDATE
				operation = "U"
				app.doprint ("Updating footnote type " + str(footnote_type_id))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting footnote type " + str(footnote_type_id))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating footnote type " + str(footnote_type_id))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO footnote_types_oplog (footnote_type_id, validity_start_date,
				validity_end_date, application_code, operation, operation_date, national)
				VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
				(footnote_type_id, validity_start_date, validity_end_date, application_code, operation, operation_date, national))
				app.conn.commit()
			except:
				g.app.log_error("footnote_type", operation, None, footnote_type_id, transaction_id, message_id)
			cur.close()
