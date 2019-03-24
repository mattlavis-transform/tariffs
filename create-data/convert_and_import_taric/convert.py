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

if (len(sys.argv) > 8):
	sMerge7 = sys.argv[8]
else:
	sMerge7 = ""

if (len(sys.argv) > 9):
	sMerge8 = sys.argv[9]
else:
	sMerge8 = ""

if (len(sys.argv) > 10):
	sMerge9 = sys.argv[10]
else:
	sMerge9 = ""

if (len(sys.argv) > 11):
	sMerge10 = sys.argv[11]
else:
	sMerge10 = ""

#print (sMerge8)
#sys.exit()

app.endDateEUMeasures(sXMLFile, sMerge1, sMerge2, sMerge3, sMerge4, sMerge5, sMerge6, sMerge7, sMerge8, sMerge9, sMerge10)
app.generateMetadata()
