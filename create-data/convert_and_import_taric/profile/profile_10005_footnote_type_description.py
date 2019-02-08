import psycopg2
import common.globals as g

class profile_10005_footnote_type_description(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                  = app.getDatestamp()
		footnote_type_id				= app.getValue(oMessage, ".//oub:footnote.type.id", True)
		language_id						= app.getValue(oMessage, ".//oub:language.id", True)
		description						= app.getValue(oMessage, ".//oub:description", True)

		if update_type == "20":
			app.doprint ("Deleting footnote type description " + str(footnote_type_id))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM footnote_type_descriptions_oplog WHERE footnote_type_id = %s", (footnote_type_id,))
				app.conn.commit()
			except:
				g.app.log_error("footnote_type_description", "D", None, footnote_type_id, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":		# UPDATE
				operation = "U"
				app.doprint ("Updating footnote type description " + str(footnote_type_id))
			elif update_type == "2":	# DELETE
				operation = "U"
				app.doprint ("Deleting footnote type description " + str(footnote_type_id))
			else:						# INSERT
				operation = "C"
				app.doprint ("Creating footnote type description " + str(footnote_type_id))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO footnote_type_descriptions_oplog (footnote_type_id, language_id,
				description, operation, operation_date)
				VALUES (%s, %s, %s, %s, %s)""", 
				(footnote_type_id, language_id,
				description, operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("footnote_type_description", operation, None, footnote_type_id, transaction_id, message_id)
			cur.close()
