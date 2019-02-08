import functions

#######################################################################################################
# GET ADDITIONAL CODE DESCRIPTION PERIODS
# 001604202024505+0000000130000972800012351B92211062018'
#######################################################################################################

namespaces = functions.namespaces
sDivider = functions.sDivider

def convert(root):
	global namespaces
	global sDivider

	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:additional.code.description.period/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:additional.code.description.period/oub:additional.code.description.period.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:additional.code.description.period/oub:additional.code.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:additional.code.description.period/oub:additional.code.type.id", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:additional.code.description.period/oub:additional.code", 3, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:additional.code.description.period/oub:validity.start.date", 8, "0", functions.datatype.date)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)