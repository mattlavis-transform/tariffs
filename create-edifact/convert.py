# Import external libraries
import xml.etree.ElementTree as ET
import csv
import sys

# Import custom libraries
import functions

if (len(sys.argv) > 1):
	sXMLFile = sys.argv[1]
	functions.doConvert(sXMLFile)
	
