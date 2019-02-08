import psycopg2
import common.globals as g

class profile_43020_footnote_association_measure(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date      = app.getDatestamp()
		measure_sid			= app.getNumberValue(oMessage, ".//oub:measure.sid", True)
		footnote_type_id	= app.getValue(oMessage, ".//oub:footnote.type.id", True)
		footnote_id	        = app.getValue(oMessage, ".//oub:footnote.id", True)

		if update_type == "20":
			app.doprint ("Deleting footnote association with measure " + str(measure_sid))
			cur = app.conn.cursor()
			try:
				cur.execute("""DELETE FROM footnote_association_measures_oplog WHERE measure_sid = %s
				AND footnote_type_id = %s AND footnote_id = %s""", (measure_sid, footnote_type_id, footnote_id))
				app.conn.commit()
			except:
				g.app.log_error("footnote association with measure", "D", measure_sid, None, transaction_id, message_id)
			cur.close()

		else:
			if measure_sid < 0:
				national = True
			else:
				national = None
			if update_type == "1":		# UPDATE
				operation = "U"
				app.doprint ("Updating footnote association with measure " + str(measure_sid))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting footnote association with measure " + str(measure_sid))
			else:						# INSERT
				operation = "C"
				app.doprint ("Creating footnote association with measure " + str(measure_sid))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO footnote_association_measures_oplog (measure_sid,
				footnote_type_id, footnote_id, operation, operation_date, national)
				VALUES (%s, %s, %s, %s, %s, %s)""", 
				(measure_sid, footnote_type_id, footnote_id, operation, operation_date, national))
				app.conn.commit()
			except:
				g.app.log_error("footnote association with measure", operation, measure_sid, None, transaction_id, message_id)
			cur.close()
