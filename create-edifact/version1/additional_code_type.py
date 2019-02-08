import functions

#######################################################################################################
# GET ADDITIONAL CODE TYPE
#######################################################################################################

namespaces = functions.namespaces
sDivider = functions.sDivider

def convert(root):
	global namespaces
	global sDivider

	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:additional.code.type/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:additional.code.type/oub:additional.code.type.id", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:additional.code.type/oub:validity.start.date", 8, "0", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:additional.code.type/oub:validity.end.date", 8, "0", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:additional.code.type/oub:application.code", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:additional.code.type/meursing.table.plan.id", 2, "0", functions.datatype.string)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)