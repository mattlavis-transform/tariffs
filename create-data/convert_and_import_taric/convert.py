# Import external libraries
import xml.etree.ElementTree as ET
import common.globals as g
import csv
import sys

app = g.app

if (len(sys.argv) > 1):
	sXMLFile = sys.argv[1]
else:
	sys.exit()

if (len(sys.argv) > 2):
	sMerge1 = sys.argv[2]
else:
	sMerge1 = ""

if (len(sys.argv) > 3):
	sMerge2 = sys.argv[3]
else:
	sMerge2 = ""
	
if (len(sys.argv) > 3):
	sMerge3 = sys.argv[3]
else:
	sMerge3 = ""
	
app.endDateEUMeasures(sXMLFile, sMerge1, sMerge2, sMerge3)
app.generateMetadata()
