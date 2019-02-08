import functions

#######################################################################################################
# GET MEASURES
# 001604272243000+00000008103639359490   10110702000000           090620181R1708920110620181R170892000000040000030256                '
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:measure/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider

		sOut += functions.edi(oNode, "oub:measure/oub:measure.sid",                        8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:measure.type",                       6, " ", functions.datatype.string, "left") + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:geographical.area",                  4, " ", functions.datatype.string, "left") + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:goods.nomenclature.item.id",        10, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:additional.code.type",               1, " ", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:additional.code",                    3, " ", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:ordernumber",                        6, " ", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:reduction.indicator",                1, " ", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:validity.start.date",                8, " ", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:measure.generating.regulation.role", 1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:measure.generating.regulation.id",   8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:validity.end.date",                  8, "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:justification.regulation.role",      1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:justification.regulation.id",        8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:stopped.flag",                       1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:geographical.area.sid",              8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:goods.nomenclature.sid",             8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:additional.code.sid",                8, " ", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure/oub:export.refund.nomenclature.sid",     8, " ", functions.datatype.string) + functions.sDivider
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)