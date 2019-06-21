from __future__ import with_statement
import psycopg2
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
import os
import sys
import codecs
import re
import functions

conn = psycopg2.connect("dbname=trade_tariff_1809 user=postgres password=" + self.p)

functions.getAllMeasurementUnitQualifiers(app)

sSQL = """SELECT m.goods_nomenclature_item_id, m.measure_type_id, mc.duty_expression_id, mc.duty_amount, mc.monetary_unit_code,
mc.measurement_unit_code, mc.measurement_unit_qualifier_code, m.validity_start_date, m.validity_end_date, m.geographical_area_id
FROM measure_components mc, ml.v5_2019 m
WHERE mc.measure_sid = m.measure_sid
/*AND m.validity_start_date < CURRENT_DATE
AND (m.validity_end_date > CURRENT_DATE OR m.validity_end_date IS NULL)*/
AND m.measure_type_id IN ('103', '105')
ORDER BY m.goods_nomenclature_item_id, mc.duty_expression_id"""
cur = conn.cursor()
cur.execute(sSQL)
rows_duties = cur.fetchall()

# Do a pass through the duties table and create a full duty expression
rdList = []
sOutQual = ""
for rd in rows_duties:
	sCommodityCode                = rd[0]
	sMeasureTypeId                = rd[1]
	sDutyExpression               = str(rd[2])
	sDutyAmount                   = str(rd[3])
	sMonetaryUnitCode             = str(rd[4])
	sMonetaryUnitCode             = sMonetaryUnitCode.replace("EUR", "€")
	sMeasurementUnitCode          = functions.getMeasurementUnit(str(rd[5]))
	sMeasurementUnitQualifierCode = str(rd[6])
	sFullExpression = sDutyAmount
	if (sMonetaryUnitCode == "" or sMonetaryUnitCode == "None"):
		sFullExpression += "%"
	else:
		sFullExpression += " " + sMonetaryUnitCode
		
	if (sMeasurementUnitCode != "" and sMeasurementUnitCode != "None"):
		sFullExpression += " / " + sMeasurementUnitCode

	# print (sFullExpression)
	if sMeasurementUnitQualifierCode != "None":
		print (sMeasurementUnitQualifierCode)
		sOutQual = sOutQual + sMeasurementUnitQualifierCode + "|" + sCommodityCode + "\n"
		
	rdList.append([sCommodityCode, sDutyExpression, sDutyAmount, sMonetaryUnitCode, sMeasurementUnitCode, sMeasurementUnitQualifierCode, sFullExpression, "Active"])
	
# Now, do a pass through the duties table and join up where there are multiple
sCommodityCodeOld = ""
sOut = ""
print (len(rdList))
for x in range(1, len(rdList) - 1):
	sCommodityCode = rdList[x][0]
	sDutyExpression = str(rdList[x][1])
	sDutyAmount = str(rdList[x][2])
	sMonetaryUnitCode = str(rdList[x][3])
	sMeasurementUnitCode = str(rdList[x][4])
	sMeasurementUnitQualifierCode = str(rdList[x][5])
	sFullExpression = str(rdList[x][6])
	
	if (sCommodityCodeOld == sCommodityCode):
		rdList[x - 1][6] += " + " + rdList[x][6]
		rdList[x][7] = "Inactive"
	
		for rd in rdList:
			sCommodityCode2 = rd[0]
			sActive = rd[7]
			if (sCommodityCode == sCommodityCode2 and sActive == "Active"):
				if (rd[6] == "") or (rd[6] == "0.0%"):
					sDuty = "Free"
				else:
					sDuty = str(rd[6])
				break
		sOut = sOut + sCommodityCode + " : " + sDuty

conn.close()

file = codecs.open("C:\\projects\\create_tariff_schedule\\test\\duty\\duties.txt", "w", "utf-8") 
file.write(sOut) 

file = codecs.open("C:\\projects\\create_tariff_schedule\\test\\duty\\qual.txt", "w", "utf-8") 
file.write(sOutQual) 
