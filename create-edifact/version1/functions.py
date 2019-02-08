import sys
import enum

global iCount
global dictRecordCount

namespaces = {'oub': 'urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0', 'env': 'urn:publicid:-:DGTAXUD:GENERAL:ENVELOPE:1.0', } # add more as needed
sDivider = ""

class datatype(enum.Enum):
    string = 1
    date = 2
    currency = 3

def tofloat(s):
	try:
		return float(s)
	except ValueError:
		return 0
	
def todate(s):
	t = s[8:] + s[5:7] + s[0:4]	
	return (t)

def edi(oNode, sFind, length, defaultChar, fieldType, direction="right"):
	# sys.exit()
	global namespaces
	try:
		value = oNode.find(sFind, namespaces).text
		
		if (fieldType == datatype.currency):
			v2 = int(tofloat(value) * 1000)
			value = str(v2)
		elif (fieldType == datatype.date):
			value = todate(value)
		else:
			value = value.replace("\n", "<P>")

		if (length != "-1"):
			if (direction == "right"):
				value = value.rjust(length, defaultChar)
			else:
				value = value.ljust(length, defaultChar)
	except:
		#print ("oh no")
		if (length != "-1"):
			value = defaultChar * length
		else:
			value = ""

	return (value)
	
	
def updateRecordCount(key, value):
	global dictRecordCount
	if key != "":
		if key in dictRecordCount:
			dictRecordCount[key] += value
		else:
			dictRecordCount[key] = value
