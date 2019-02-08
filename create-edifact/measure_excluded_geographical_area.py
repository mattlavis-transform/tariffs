import functions

#######################################################################################################
# GET FOOTNOTE ASSOCIATION MEASURE
# 001604275643020+00000028303639381TM 872  '
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:measure.excluded.geographical.area/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider

		sOut += functions.edi(oNode, "oub:measure.excluded.geographical.area/oub:measure.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.excluded.geographical.area/oub:excluded.geographical.area", 4, " ", functions.datatype.string, "left") + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.excluded.geographical.area/oub:geographical.area.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
