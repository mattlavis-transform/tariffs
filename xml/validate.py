import psycopg2
import sys
import os
import xmlschema
from xml.sax.saxutils import escape

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font, NamedStyle

path = "/Users/matt.admin/projects/tariffs/xml/sample.xml"
path = "/Users/matt.admin/projects/tariffs/xml/Geographical area xml.xml"

schema_path =  "envelope.xsd"
my_schema = xmlschema.XMLSchema(schema_path)

try:
	if my_schema.is_valid(path):
		print ("The file validated successfully.")
	else:
		print ("The file did not validate.")
except:
	print ("The file did not validate and crashed the validator.")
