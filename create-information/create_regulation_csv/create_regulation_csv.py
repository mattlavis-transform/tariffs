import psycopg2
import os
import sys

#from application import application
import functions as f

conn = psycopg2.connect("dbname=trade_tariff_181212b user=postgres password" + self.p)

sSQL = """SELECT DISTINCT regulation_id FROM ml.v5_2019 as m WHERE regulation_id > 'IYY9999' AND regulation_id != 'IYY9999' ORDER BY 1"""
cur = conn.cursor()
cur.execute(sSQL)
rows_regulations = cur.fetchall()
i = 1
for m in rows_regulations:
	sRegulationID = m[0]
	print ("Creating document for regulation " + sRegulationID)
	f.app.createRegulationCSV(sRegulationID) 
	i = i + 1
	if i > 1000:
		sys.exit()

conn.close()
