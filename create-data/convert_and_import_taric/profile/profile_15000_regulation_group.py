import psycopg2
import sys
from datetime import datetime
import common.globals as g

class profile_15000_regulation_group(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date		        = app.getDatestamp()
		regulation_group_id         = app.getValue(oMessage, ".//oub:regulation.group.id", True)
		validity_start_date	        = app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		validity_end_date	        = app.getDateValue(oMessage, ".//oub:validity.end.date", True)

		if update_type == "1":	    # UPDATE
			operation = "U"
			app.doprint ("Updating regulation group " + str(regulation_group_id))
		elif update_type == "2":	# DELETE
			operation = "D"
			app.doprint ("Deleting regulation group " + str(regulation_group_id))
		else:					    # INSERT
			operation = "C"
			app.doprint ("Creating regulation group " + str(regulation_group_id))

		cur = app.conn.cursor()
		try:
			cur.execute("""INSERT INTO regulation_groups_oplog (regulation_group_id, validity_start_date,
			validity_end_date, operation, operation_date)
			VALUES (%s, %s, %s, %s, %s, %s)""", 
			(regulation_group_id, validity_start_date, validity_end_date, operation, operation_date))
			app.conn.commit()
		except:
			g.app.log_error("regulation group", operation, None, regulation_group_id, transaction_id, message_id)
		cur.close()
