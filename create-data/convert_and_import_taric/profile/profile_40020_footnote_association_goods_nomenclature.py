import psycopg2
import common.globals as g

class profile_40020_footnote_association_goods_nomenclature(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date				= app.getDatestamp()
		goods_nomenclature_sid		= app.getNumberValue(oMessage, ".//oub:goods_nomenclature.sid", True)
		footnote_type				= app.getValue(oMessage, ".//oub:footnote.type", True)
		footnote_id	        		= app.getValue(oMessage, ".//oub:footnote.id", True)
		validity_start_date			= app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		validity_end_date			= app.getDateValue(oMessage, ".//oub:validity.end.date", True)
		goods_nomenclature_item_id	= app.getValue(oMessage, ".//oub:goods.nomenclature.item.id", True)
		productline_suffix			= app.getValue(oMessage, ".//oub:productline.suffix", True)

		if update_type == "20":
			app.doprint ("Deleting footnote association goods nomenclature " + str(goods_nomenclature_sid))
			cur = app.conn.cursor()
			try:
				cur.execute("""DELETE FROM footnote_association_goods_nomenclatures_oplog
				WHERE goods_nomenclature_sid = %s
				AND footnote_type = %s
				AND footnote_id = %s""", (goods_nomenclature_sid, footnote_type, footnote_id))
				app.conn.commit()
			except:
				g.app.log_error("footnote association goods nomenclature", "D", goods_nomenclature_sid, goods_nomenclature_item_id, transaction_id, message_id)
			cur.close()

		else:
			if update_type == "1":		# Update
				operation = "U"
				app.doprint ("Updating footnote association goods nomenclature " + str(goods_nomenclature_sid))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting footnote association goods nomenclature " + str(goods_nomenclature_sid))
			else:						# INSERT
				operation = "C"
				app.doprint ("Creating footnote association goods nomenclature " + str(goods_nomenclature_sid))

			cur = app.conn.cursor()
			try:
				cur.execute("""INSERT INTO footnote_association_goods_nomenclatures_oplog (goods_nomenclature_sid,
				footnote_type, footnote_id, validity_start_date, validity_end_date,
				goods_nomenclature_item_id, productline_suffix,
				operation, operation_date)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
				(goods_nomenclature_sid,
				footnote_type, footnote_id, validity_start_date, validity_end_date,
				goods_nomenclature_item_id, productline_suffix,
				operation, operation_date))
				app.conn.commit()
			except:
				g.app.log_error("footnote association goods nomenclature", operation, goods_nomenclature_sid, goods_nomenclature_item_id, transaction_id, message_id)
			cur.close()
