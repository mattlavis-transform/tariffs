import psycopg2
import common.globals as g

class profile_29500_prorogation_regulation(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date						= app.getDatestamp()
		prorogation_regulation_role		= app.getValue(oMessage, ".//oub:prorogation.regulation.role", True)
		prorogation_regulation_id		= app.getValue(oMessage, ".//oub:prorogation.regulation.id", True)
		published_date		        	= app.getDateValue(oMessage, ".//oub:published.date", True)
		officialjournal_number			= app.getValue(oMessage, ".//oub:officialjournal.number", True)
		officialjournal_page	        = app.getValue(oMessage, ".//oub:officialjournal.page", True)
		replacement_indicator           = app.getValue(oMessage, ".//oub:replacement.indicator", True)
		information_text                = app.getValue(oMessage, ".//oub:information.text", True)
		approved_flag                  	= app.getValue(oMessage, ".//oub:approved.flag", True)

		if update_type == "20":
			app.doprint ("Deleting prorogation regulation " + str(prorogation_regulation_id))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM prorogation_regulations_oplog WHERE prorogation_regulation_id = %s", (prorogation_regulation_id,))
				app.conn.commit()
			except:
				g.app.log_error("prorogation regulation", "D", None, prorogation_regulation_id, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":	# Update
				operation = "U"
				app.doprint ("Updating prorogation regulation " + str(prorogation_regulation_id))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting prorogation regulation " + str(prorogation_regulation_id))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating prorogation regulation " + str(prorogation_regulation_id))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO prorogation_regulations_oplog (prorogation_regulation_role,
				prorogation_regulation_id, published_date, officialjournal_number,
				officialjournal_page, replacement_indicator, information_text, approved_flag,
				operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
				(prorogation_regulation_role,
				prorogation_regulation_id, published_date, officialjournal_number,
				officialjournal_page, replacement_indicator, information_text, approved_flag,
				operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("prorogation regulation", operation, None, prorogation_regulation_id, transaction_id, message_id)
			cur.close()
