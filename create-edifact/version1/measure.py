import functions

#######################################################################################################
# GET MEASURES
# 001604272243000+00000008103639359490   10110702000000           090620181R1708920110620181R170892000000040000030256                '
#######################################################################################################

namespaces = functions.namespaces
sDivider = functions.sDivider

def convert(root):
	global namespaces
	global sDivider

	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:measure/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:measure/oub:measure.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure/oub:measure.type", 3, "0", functions.datatype.string)
		sOut += "   "
		sOut += functions.edi(oNode, "oub:measure/oub:geographical.area", 4, " ", functions.datatype.string, "left")
		sOut += functions.edi(oNode, "oub:measure/oub:goods.nomenclature.item.id", 10, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure/oub:validity.start.date", 19, " ", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:measure/oub:measure.generating.regulation.role", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure/oub:measure.generating.regulation.id", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure/oub:validity.end.date", 8, "0", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:measure/oub:justification.regulation.role", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure/oub:justification.regulation.id", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure/oub:stopped.flag", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure/oub:geographical.area.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure/oub:goods.nomenclature.sid", 8, "0", functions.datatype.string)
		sOut += " " * 16
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
	
