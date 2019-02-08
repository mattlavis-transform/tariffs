import functions

#######################################################################################################
# GET ADDITIONAL CODE DESCRIPTION PERIODS
# 001604202024505+0000000130000972800012351B92211062018'
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:additional.code.description.period/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:additional.code.description.period/oub:additional.code.description.period.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:additional.code.description.period/oub:additional.code.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:additional.code.description.period/oub:additional.code.type.id", 1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:additional.code.description.period/oub:additional.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:additional.code.description.period/oub:validity.start.date", 8, "0", functions.datatype.date) + functions.sDivider
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
