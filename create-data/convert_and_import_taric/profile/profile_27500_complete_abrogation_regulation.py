import psycopg2
import common.globals as g

class profile_27500_complete_abrogation_regulation(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date						= app.getDatestamp()
		complete_abrogation_regulation_role	= app.getValue(oMessage, ".//oub:complete.abrogation.regulation.role", True)
		complete_abrogation_regulation_id	= app.getValue(oMessage, ".//oub:complete.abrogation.regulation.id", True)
		published_date		        		= app.getDateValue(oMessage, ".//oub:published.date", True)
		officialjournal_number			    = app.getValue(oMessage, ".//oub:officialjournal.number", True)
		officialjournal_page	            = app.getValue(oMessage, ".//oub:officialjournal.page", True)
		replacement_indicator               = app.getValue(oMessage, ".//oub:replacement.indicator", True)
		information_text                  	= app.getValue(oMessage, ".//oub:information.text", True)
		approved_flag                  		= app.getValue(oMessage, ".//oub:approved.flag", True)

		if update_type == "20":
			app.doprint ("Deleting complete abrogation regulation " + str(complete_abrogation_regulation_id))
			cur = app.conn.cursor()
			try:
				cur.execute("""DELETE FROM complete_abrogation_regulations_oplog WHERE complete_abrogation_regulation_id = %s
				AND complete_abrogation_regulation_role = %s""", (complete_abrogation_regulation_id, complete_abrogation_regulation_role,))
				app.conn.commit()
			except:
				g.app.log_error("complete abrogation regulation", "D", None, complete_abrogation_regulation_id, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":	# Update
				operation = "U"
				app.doprint ("Updating complete abrogation regulation " + str(complete_abrogation_regulation_id))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting complete abrogation regulation " + str(complete_abrogation_regulation_id))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating complete abrogation regulation " + str(complete_abrogation_regulation_id))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO complete_abrogation_regulations_oplog (complete_abrogation_regulation_role,
				complete_abrogation_regulation_id, published_date, officialjournal_number,
				officialjournal_page, replacement_indicator, information_text, approved_flag,
				operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
				(complete_abrogation_regulation_role,
				complete_abrogation_regulation_id, published_date, officialjournal_number,
				officialjournal_page, replacement_indicator, information_text, approved_flag,
				operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("complete abrogation regulation", operation, None, complete_abrogation_regulation_id, transaction_id, message_id)
			cur.close()
