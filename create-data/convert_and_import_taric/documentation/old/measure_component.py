import functions

#######################################################################################################
# GET MEASURE COMPONENTS
# 001604275643005+00000027303639381010000130500EURDTN '
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:measure.component/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider

		sOut += functions.edi(oNode, "oub:measure.component/oub:measure.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.component/oub:duty.expression.id", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.component/oub:duty.amount", 10, "0", functions.datatype.currency) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.component/oub:monetary.unit.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.component/oub:measurement.unit.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += " '\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
