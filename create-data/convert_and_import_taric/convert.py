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

if (len(sys.argv) > 12):
	sMerge11 = sys.argv[12]
else:
	sMerge11 = ""

if (len(sys.argv) > 13):
	sMerge12 = sys.argv[13]
else:
	sMerge12 = ""

if (len(sys.argv) > 14):
	sMerge13 = sys.argv[14]
else:
	sMerge13 = ""

if (len(sys.argv) > 15):
	sMerge14 = sys.argv[15]
else:
	sMerge14 = ""

if (len(sys.argv) > 16):
	sMerge15 = sys.argv[16]
else:
	sMerge15 = ""

if (len(sys.argv) > 17):
	sMerge16 = sys.argv[17]
else:
	sMerge16 = ""

if (len(sys.argv) > 18):
	sMerge17 = sys.argv[18]
else:
	sMerge17 = ""

if (len(sys.argv) > 19):
	sMerge18 = sys.argv[19]
else:
	sMerge18 = ""

if (len(sys.argv) > 20):
	sMerge19 = sys.argv[20]
else:
	sMerge19 = ""

if (len(sys.argv) > 21):
	sMerge20 = sys.argv[21]
else:
	sMerge20 = ""

#print (sMerge8)
#sys.exit()

app.endDateEUMeasures(sXMLFile, sMerge1, sMerge2, sMerge3, sMerge4, sMerge5, sMerge6, sMerge7, sMerge8, sMerge9, sMerge10, sMerge11, sMerge12, sMerge13, sMerge14, sMerge15, sMerge16, sMerge17, sMerge18, sMerge19, sMerge20)
app.generateMetadata()
