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
	
if (len(sys.argv) > 4):
	sMerge3 = sys.argv[4]
else:
	sMerge3 = ""
	
if (len(sys.argv) > 5):
	sMerge4 = sys.argv[5]
else:
	sMerge4 = ""
	
if (len(sys.argv) > 6):
	sMerge5 = sys.argv[6]
else:
	sMerge5 = ""
	
if (len(sys.argv) > 7):
	sMerge6 = sys.argv[7]
else:
	sMerge6 = ""
	
app.endDateEUMeasures(sXMLFile, sMerge1, sMerge2, sMerge3, sMerge4, sMerge5, sMerge6)
app.generateMetadata()
