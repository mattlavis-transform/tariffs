import psycopg2
import common.globals as g

class profile_20000_footnote(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date				= app.getDatestamp()
		footnote_type_id			= app.getValue(oMessage, ".//oub:footnote.type.id", True)
		footnote_id					= app.getValue(oMessage, ".//oub:footnote.id", True)
		validity_start_date			= app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		validity_end_date			= app.getDateValue(oMessage, ".//oub:validity.end.date", True)

		if update_type == "20":
			app.doprint ("Deleting footnote " + str(footnote_id))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM footnotes_oplog WHERE footnote_id = %s AND footnote_type_id = %s", (footnote_id, footnote_type_id,))
				app.conn.commit()
			except:
				g.app.log_error("footnote", "D", None, footnote_type_id + "|" + footnote_id, transaction_id, message_id)
			cur.close()

		else:
			if footnote_type_id in ('01', '02', '03', '05', '05', '06'):
				national = True
			else:
				national = None
			if update_type == "1":	# UPDATE
				operation = "U"
				app.doprint ("Updating footnote " + str(footnote_id))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting footnote " + str(footnote_id))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating footnote " + str(footnote_id))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO footnotes_oplog (footnote_type_id, footnote_id, validity_start_date,
				validity_end_date, operation, operation_date, national)
				VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
				(footnote_type_id, footnote_id, validity_start_date, validity_end_date, operation, operation_date, national))
				app.conn.commit()
			except:
				g.app.log_error("footnote", operation, None, footnote_type_id + "|" + footnote_id, transaction_id, message_id)
			cur.close()
