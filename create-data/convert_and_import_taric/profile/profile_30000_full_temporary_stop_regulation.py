import psycopg2
import common.globals as g

class profile_30000_full_temporary_stop_regulation(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date						= app.getDatestamp()
		full_temporary_stop_regulation_role	= app.getValue(oMessage, ".//oub:full.temporary.stop.regulation.role", True)
		full_temporary_stop_regulation_id	= app.getValue(oMessage, ".//oub:full.temporary.stop.regulation.id", True)
		published_date		        		= app.getDateValue(oMessage, ".//oub:published.date", True)
		officialjournal_number			    = app.getValue(oMessage, ".//oub:officialjournal.number", True)
		officialjournal_page	            = app.getValue(oMessage, ".//oub:officialjournal.page", True)
		validity_start_date					= app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		validity_end_date					= app.getDateValue(oMessage, ".//oub:validity.end.date", True)
		effective_enddate					= app.getDateValue(oMessage, ".//oub:effective.enddate", True)
		complete_abrogation_regulation_role	= app.getValue(oMessage, ".//oub:complete.abrogation.regulation.role", True)
		complete_abrogation_regulation_id	= app.getValue(oMessage, ".//oub:complete.abrogation.regulation.id", True)
		explicit_abrogation_regulation_role	= app.getValue(oMessage, ".//oub:explicit.abrogation.regulation.role", True)
		explicit_abrogation_regulation_id	= app.getValue(oMessage, ".//oub:explicit.abrogation.regulation.id", True)
		replacement_indicator               = app.getValue(oMessage, ".//oub:replacement.indicator", True)
		information_text                  	= app.getValue(oMessage, ".//oub:information.text", True)
		approved_flag                  		= app.getValue(oMessage, ".//oub:approved.flag", True)

		if update_type == "20":
			app.doprint ("Deleting full temporary stop regulation " + str(full_temporary_stop_regulation_id))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM full_temporary_stop_regulations_oplog WHERE full_temporary_stop_regulation_id = %s", (full_temporary_stop_regulation_id,))
				app.conn.commit()
			except:
				g.app.log_error("full temporary stop regulation", "D", None, full_temporary_stop_regulation_id, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":	# UPDATE
				operation = "U"
				app.doprint ("Updating full temporary stop regulation " + str(full_temporary_stop_regulation_id))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting full temporary stop regulation " + str(full_temporary_stop_regulation_id))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating full temporary stop regulation " + str(full_temporary_stop_regulation_id))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO full_temporary_stop_regulations_oplog (full_temporary_stop_regulation_role,
				full_temporary_stop_regulation_id, published_date, officialjournal_number,
				officialjournal_page,
				validity_start_date, validity_end_date, effective_enddate, 
				complete_abrogation_regulation_role, complete_abrogation_regulation_id,
				explicit_abrogation_regulation_role, explicit_abrogation_regulation_id,
				replacement_indicator, information_text, approved_flag,
				operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
				(full_temporary_stop_regulation_role,
				full_temporary_stop_regulation_id, published_date, officialjournal_number,
				officialjournal_page,
				validity_start_date, validity_end_date, effective_enddate, 
				complete_abrogation_regulation_role, complete_abrogation_regulation_id,
				explicit_abrogation_regulation_role, explicit_abrogation_regulation_id,
				replacement_indicator, information_text, approved_flag,
				operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("full temporary stop regulation", operation, None, full_temporary_stop_regulation_id, transaction_id, message_id)
			cur.close()
