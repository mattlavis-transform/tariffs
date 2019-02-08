import psycopg2
import common.globals as g

class profile_28000_explicit_abrogation_regulation(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date						= app.getDatestamp()
		explicit_abrogation_regulation_role	= app.getValue(oMessage, ".//oub:explicit.abrogation.regulation.role", True)
		explicit_abrogation_regulation_id	= app.getValue(oMessage, ".//oub:explicit.abrogation.regulation.id", True)
		published_date		        		= app.getDateValue(oMessage, ".//oub:published.date", True)
		officialjournal_number			    = app.getValue(oMessage, ".//oub:officialjournal.number", True)
		officialjournal_page	            = app.getValue(oMessage, ".//oub:officialjournal.page", True)
		replacement_indicator               = app.getValue(oMessage, ".//oub:replacement.indicator", True)
		abrogation_date		        		= app.getDateValue(oMessage, ".//oub:abrogation.date", True)
		information_text                  	= app.getValue(oMessage, ".//oub:information.text", True)
		approved_flag                  		= app.getValue(oMessage, ".//oub:approved.flag", True)

		if update_type == "20":
			app.doprint ("Deleting explicit abrogation regulation " + str(explicit_abrogation_regulation_id))
			cur = app.conn.cursor()
			try:
				cur.execute("""DELETE FROM explicit_abrogation_regulations_oplog WHERE explicit_abrogation_regulation_id = %s
				AND explicit_abrogation_regulation_role = %s""", (explicit_abrogation_regulation_id, explicit_abrogation_regulation_role,))
				app.conn.commit()
			except:
				g.app.log_error("explicit abrogation regulation", "D", None, explicit_abrogation_regulation_id, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":	# Update
				operation = "U"
				app.doprint ("Updating explicit abrogation regulation " + str(explicit_abrogation_regulation_id))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting explicit abrogation regulation " + str(explicit_abrogation_regulation_id))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating explicit abrogation regulation " + str(explicit_abrogation_regulation_id))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO explicit_abrogation_regulations_oplog (explicit_abrogation_regulation_role,
				explicit_abrogation_regulation_id, published_date, officialjournal_number,
				officialjournal_page, replacement_indicator, abrogation_date, information_text, approved_flag,
				operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
				(explicit_abrogation_regulation_role,
				explicit_abrogation_regulation_id, published_date, officialjournal_number,
				officialjournal_page, replacement_indicator, abrogation_date, information_text, approved_flag,
				operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("explicit abrogation regulation", operation, None, explicit_abrogation_regulation_id, transaction_id, message_id)
			cur.close()
