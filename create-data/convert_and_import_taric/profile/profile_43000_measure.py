import psycopg2
import common.globals as g

class profile_43000_measure(object):
	def import_xml(self, app, update_type, oMessage, transaction_id, message_id):
		g.app.message_count += 1
		operation_date                      = app.getDatestamp()
		measure_sid							= app.getNumberValue(oMessage, ".//oub:measure.sid", True)
		measure_type						= app.getValue(oMessage, ".//oub:measure.type", True)
		geographical_area					= app.getValue(oMessage, ".//oub:geographical.area", True)
		goods_nomenclature_item_id			= app.getValue(oMessage, ".//oub:goods.nomenclature.item.id", True)
		additional_code_type				= app.getValue(oMessage, ".//oub:additional.code.type", True)
		additional_code						= app.getValue(oMessage, ".//oub:additional.code", True)
		ordernumber							= app.getValue(oMessage, ".//oub:ordernumber", True)
		reduction_indicator					= app.getNumberValue(oMessage, ".//oub:reduction.indicator", True)
		validity_start_date					= app.getDateValue(oMessage, ".//oub:validity.start.date", True)
		measure_generating_regulation_role	= app.getValue(oMessage, ".//oub:measure.generating.regulation.role", True)
		measure_generating_regulation_id	= app.getValue(oMessage, ".//oub:measure.generating.regulation.id", True)
		validity_end_date					= app.getDateValue(oMessage, ".//oub:validity.end.date", True)
		justification_regulation_role		= app.getValue(oMessage, ".//oub:justification.regulation.role", True)
		justification_regulation_id			= app.getValue(oMessage, ".//oub:justification.regulation.id", True)
		stopped_flag						= app.getValue(oMessage, ".//oub:stopped.flag", True)
		geographical_area_sid				= app.getNumberValue(oMessage, ".//oub:geographical.area.sid", True)
		goods_nomenclature_sid				= app.getNumberValue(oMessage, ".//oub:goods.nomenclature.sid", True)
		additional_code_sid					= app.getNumberValue(oMessage, ".//oub:additional.code.sid", True)
		export_refund_nomenclature_sid		= app.getNumberValue(oMessage, ".//oub:export.refund.nomenclature.sid", True)

		tariff_measure_number = goods_nomenclature_item_id
		if goods_nomenclature_item_id != None:
			if tariff_measure_number[-2:] == "00":
				tariff_measure_number = tariff_measure_number[:-2]

		if update_type == "20":
			app.doprint ("Deleting measure " + str(measure_sid))
			cur = app.conn.cursor()
			try:
				cur.execute("DELETE FROM measures_oplog WHERE measure_sid = %s", (measure_sid,))
				app.conn.commit()
			except:
				g.app.log_error("measure", "D", measure_sid, None, transaction_id, message_id)
			cur.close()

		else:
			if measure_sid < 0:
				national = True
			else:
				national = None
			if update_type == "1":	# Update
				operation = "U"
				app.doprint ("Updating measure " + str(measure_sid))
			elif update_type == "2":	# DELETE
				operation = "D"
				app.doprint ("Deleting measure " + str(measure_sid))
			else:					# INSERT
				operation = "C"
				app.doprint ("Creating measure " + str(measure_sid))

			cur = app.conn.cursor()
			#try:
			cur.execute("""INSERT INTO measures_oplog (measure_sid, measure_type_id, geographical_area_id,
			goods_nomenclature_item_id, additional_code_type_id, additional_code_id,
			ordernumber, reduction_indicator, validity_start_date,
			measure_generating_regulation_role, measure_generating_regulation_id, validity_end_date,
			justification_regulation_role, justification_regulation_id, stopped_flag,
			geographical_area_sid, goods_nomenclature_sid, additional_code_sid,
			export_refund_nomenclature_sid, operation, operation_date, national, tariff_measure_number)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
			(measure_sid, measure_type, geographical_area,
			goods_nomenclature_item_id, additional_code_type, additional_code,
			ordernumber, reduction_indicator, validity_start_date,
			measure_generating_regulation_role, measure_generating_regulation_id, validity_end_date,
			justification_regulation_role, justification_regulation_id, stopped_flag,
			geographical_area_sid, goods_nomenclature_sid, additional_code_sid,
			export_refund_nomenclature_sid, operation, operation_date, national, tariff_measure_number))
			app.conn.commit()
			#except:
			#	g.app.log_error("measure", operation, measure_sid, None, transaction_id, message_id)
			cur.close()
