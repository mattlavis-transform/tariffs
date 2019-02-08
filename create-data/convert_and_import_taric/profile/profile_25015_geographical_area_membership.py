import psycopg2
import common.globals as g

class profile_25015_geographical_area_membership(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date      = app.getDatestamp()
		geographical_area_sid		= app.getNumberValue(oMessage, ".//oub:geographical.area.sid", True)
		geographical_area_group_sid	= app.getValue(oMessage, ".//oub:geographical.area.group.sid", True)
		validity_start_date			= app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		validity_end_date			= app.getDateValue(oMessage, ".//oub:validity.end.date", True)

		if update_type == "20":
			app.doprint ("Deleting geographical area membership " + str(geographical_area_sid))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM geographical_area_memberships_oplog WHERE geographical_area_sid = %s AND geographical_area_group_sid = %s", (geographical_area_sid, geographical_area_group_sid,))
				app.conn.commit()
			except:
				g.app.log_error("geographical area membership", "D", geographical_area_sid, None, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":	# Update
				operation = "U"
				app.doprint ("Updating geographical area membership " + str(geographical_area_sid))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting geographical area membership " + str(geographical_area_sid))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating geographical area membership " + str(geographical_area_sid))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO geographical_area_memberships_oplog (geographical_area_sid,
				geographical_area_group_sid, validity_start_date, validity_end_date, operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s)""", 
				(geographical_area_sid,
				geographical_area_group_sid, validity_start_date, validity_end_date, operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("geographical area membership", operation, geographical_area_sid, None, transaction_id, message_id)
			cur.close()
