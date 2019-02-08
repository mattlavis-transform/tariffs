import psycopg2
import common.globals as g

class profile_20005_footnote_description_period(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date				    = app.getDatestamp()
		footnote_description_period_sid = app.getNumberValue(oMessage, ".//oub:footnote.description.period.sid", True)
		footnote_type_id			    = app.getValue(oMessage, ".//oub:footnote.type.id", True)
		footnote_id					    = app.getValue(oMessage, ".//oub:footnote.id", True)
		validity_start_date			    = app.getDateValue(oMessage, ".//oub:validity.start.date", True)

		if update_type == "20":
			app.doprint ("Deleting footnote description period " + str(footnote_id))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM footnote_description_periods_oplog WHERE footnote_description_period_sid = %s", (footnote_description_period_sid,))
				app.conn.commit()
			except:
				g.app.log_error("footnote_description_period", "D", footnote_description_period_sid, footnote_type_id + "|" + footnote_id, transaction_id, message_id)
			cur.close()

		else:
			if footnote_description_period_sid < 0:
				national = True
			else:
				national = None
			if update_type == "1":		# UPDATE
				operation = "U"
				app.doprint ("Updating footnote description period " + str(footnote_id))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting footnote description period " + str(footnote_id))
			else:						# INSERT
				operation = "C"
				app.doprint ("Creating footnote description period " + str(footnote_id))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO footnote_description_periods_oplog (footnote_description_period_sid,
				footnote_type_id, footnote_id, validity_start_date, operation, operation_date, national)
				VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
				(footnote_description_period_sid, footnote_type_id, footnote_id, validity_start_date, operation, operation_date, national))
				app.conn.commit()
			except:
				g.app.log_error("footnote_description_period", "D", footnote_description_period_sid, footnote_type_id + "|" + footnote_id, transaction_id, message_id)
			cur.close()
