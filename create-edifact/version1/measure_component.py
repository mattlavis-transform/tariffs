import functions

#######################################################################################################
# GET MEASURE COMPONENTS
# 001604275643005+00000027303639381010000130500EURDTN '
#######################################################################################################

namespaces = functions.namespaces
sDivider = functions.sDivider

def convert(root):
	global namespaces
	global sDivider

	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:measure.component/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:measure.component/oub:measure.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure.component/oub:duty.expression.id", 2, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure.component/oub:duty.amount", 10, "0", functions.datatype.currency)
		sOut += functions.edi(oNode, "oub:measure.component/oub:monetary.unit.code", 3, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure.component/oub:measurement.unit.code", 3, "0", functions.datatype.string)
		sOut += " '\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
	
