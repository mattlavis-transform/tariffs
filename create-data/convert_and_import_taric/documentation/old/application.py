import xml.etree.ElementTree as ET
import psycopg2
import sys
import os
import csv
import re
import codecs
from datetime import datetime

from measure import measure

class application(object):
	def __init__(self):
		self.BASE_DIR		= os.path.dirname(os.path.abspath(__file__))
		self.SCHEMA_DIR		= os.path.join(self.BASE_DIR, "xsd")
		self.TEMPLATE_DIR	= os.path.join(self.BASE_DIR, "templates")
		self.XML_IN_DIR		= os.path.join(self.BASE_DIR, "xml_in")
		self.XML_OUT_DIR	= os.path.join(self.BASE_DIR, "xml_out")

		self.critical_date	= datetime.strptime("2019-03-29", '%Y-%m-%d')
		self.namespaces 	= {'oub': 'urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0', 'env': 'urn:publicid:-:DGTAXUD:GENERAL:ENVELOPE:1.0', } # add more as needed
		self.envelope_id	= ""
		self.sDivider		= ""
		self.message_id		= 1

	def endDateEUMeasures(self, sXMLFile):
		print ("Creating converted file for " + sXMLFile)

		self.sXMLFile_In	= os.path.join(self.XML_IN_DIR,  sXMLFile)
		self.sXMLFile_Out	= os.path.join(self.XML_OUT_DIR, sXMLFile)

		# Load file
		tree = ET.parse(self.sXMLFile_In)
		root = tree.getroot()

		# Get envelope
		self.envelope_id = root.get("id")
		out = '<?xml version="1.0" encoding="UTF-8"?>\n'
		out += '<env:envelope xmlns="urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0" xmlns:env="urn:publicid:-:DGTAXUD:GENERAL:ENVELOPE:1.0" id="' + self.envelope_id + '">\n'

		oMeasure = measure(self, root)
		out += oMeasure.xml

		out += '</env:envelope>'

		# Write the file
		filename = os.path.join(self.XML_OUT_DIR, sXMLFile)
		f = open(filename, "w", encoding="utf-8") 
		f.write(out)
		f.close()

		sys.exit()
		iCount = 0
		# Get all transactions with measures in them
		for oTransaction in root.findall('.//oub:measure/../../../../../env:transaction', self.namespaces):
			measure_sid = oTransaction.find(".//oub:measure/oub:measure.sid", self.namespaces).text
			validity_start_date = oTransaction.find(".//oub:measure/oub:validity.start.date", self.namespaces).text
			print (measure_sid, validity_start_date)
			iCount += 1
		print ("Transaction count", iCount)
		print (ET.tostring(oTransaction.text, encoding='utf8'))
		sys.exit()

		iCount = 0
		for oNode in root.findall('.//env:transaction//oub:validity.start.date', self.namespaces):
			iCount += 1
		print ("Start date count", iCount)

		
		for oNode in root.findall('.//env:transaction', self.namespaces):
			iCount += 1
			#print ("Transaction ID", oNode.get("id"))
			for oNodeRecord in oNode.findall('.//env:app.message', self.namespaces):
				#print ("Message ID", oNodeRecord.get("id"))
				pass
			
			for oNodeRecord in oNode.findall('.//oub:record', self.namespaces):
				print ("Transaction ID (2nd)", oNodeRecord.find("oub:record.code", self.namespaces).text)
				print ("Transaction ID (2nd)", oNodeRecord.find("./*[1]", self.namespaces).tag)
				pass
			
			for oNodeRecord in oNode.findall('.//oub:record', self.namespaces):
				#print ("Transaction ID (2nd)", oNodeRecord.find(".//*[2]", self.namespaces).text)
				#print (ET.tostring(oNodeRecord, encoding='utf8'))
				pass
				#sys.exit()
			
			
			
			
			#for oNodeRecord in oNode.findall('.//oub:record', self.namespaces):
				"""
				sfind = ".//*[2]"
				try:
					ox = oNodeRecord.find(sfind, self.namespaces)
					print ("found")
					sys.exit()
				except:
					pass
				"""
			#sys.exit()

		print (iCount)
		sys.exit()


		# open a file for writing
		#oXMLFileOut = open(sXMLOut, 'w', encoding="UTF-8")
