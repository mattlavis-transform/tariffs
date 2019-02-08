import psycopg2
import common.globals as g

class profile_25000_geographical_area(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                      = app.getDatestamp()
		geographical_area_sid				= app.getNumberValue(oMessage, ".//oub:geographical.area.sid", True)
		geographical_area_id				= app.getValue(oMessage, ".//oub:geographical.area.id", True)
		validity_start_date					= app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		validity_end_date					= app.getDateValue(oMessage, ".//oub:validity.end.date", True)
		geographical_code					= app.getValue(oMessage, ".//oub:geographical.code", True)
		parent_geographical_area_group_sid	= app.getValue(oMessage, ".//oub:cerparent.geographical.area.group.sid", True)

		if update_type == "20":
			app.doprint ("Deleting geographical area " + str(geographical_area_sid))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM geographical_areas_oplog WHERE geographical_area_sid = %s", (geographical_area_sid,))
				app.conn.commit()
			except:
				g.app.log_error("geographical area", "D", geographical_area_sid, geographical_area_id, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":		# UPDATE
				operation = "U"
				app.doprint ("Updating geographical_area " + str(geographical_area_sid))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting geographical_area " + str(geographical_area_sid))
			else:						# INSERT
				operation = "C"
				app.doprint ("Creating geographical_area " + str(geographical_area_sid))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO geographical_areas_oplog (geographical_area_sid, geographical_area_id,
				validity_start_date, validity_end_date, geographical_code,
				parent_geographical_area_group_sid, operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
				(geographical_area_sid, geographical_area_id,
				validity_start_date, validity_end_date, geographical_code,
				parent_geographical_area_group_sid, operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("geographical area", operation, geographical_area_sid, geographical_area_id, transaction_id, message_id)
			cur.close()
