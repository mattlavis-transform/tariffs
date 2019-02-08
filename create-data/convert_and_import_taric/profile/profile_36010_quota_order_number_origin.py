import psycopg2
from datetime import datetime
import common.globals as g

class profile_36010_quota_order_number_origin(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                      = app.getDatestamp()
		quota_order_number_origin_sid		= app.getNumberValue(oMessage, ".//oub:quota.order.number.origin.sid", True)
		quota_order_number_sid				= app.getNumberValue(oMessage, ".//oub:quota.order.number.sid", True)
		geographical_area_id				= app.getValue(oMessage, ".//oub:geographical.area.id", True)
		validity_start_date					= app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		validity_end_date					= app.getDateValue(oMessage, ".//oub:validity.end.date", True)
		geographical_area_sid				= app.getNumberValue(oMessage, ".//oub:geographical.area.sid", True)

		if update_type == "20":
			app.doprint ("Deleting quota order number origin " + str(quota_order_number_origin_sid))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM quota_order_number_origins_oplog WHERE quota_order_number_origin_sid = %s", (quota_order_number_origin_sid,))
				app.conn.commit()
			except:
				g.app.log_error("quota order number origin", "D", quota_order_number_origin_sid, None, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":	# UPDATE
				operation = "U"
				app.doprint ("Updating quota order number origin " + str(quota_order_number_origin_sid))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting quota order number origin " + str(quota_order_number_origin_sid))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating quota order number origin " + str(quota_order_number_origin_sid))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO quota_order_number_origins_oplog (quota_order_number_origin_sid,
				quota_order_number_sid, geographical_area_id, validity_start_date, validity_end_date,
				geographical_area_sid, operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
				(quota_order_number_origin_sid,
				quota_order_number_sid, geographical_area_id, validity_start_date, validity_end_date,
				geographical_area_sid, operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("quota order number origin", operation, quota_order_number_origin_sid, None, transaction_id, message_id)
			cur.close()
