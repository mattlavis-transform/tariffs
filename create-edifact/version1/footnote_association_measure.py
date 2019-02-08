import functions

#######################################################################################################
# GET FOOTNOTE ASSOCIATION MEASURE
# 001604275643020+00000028303639381TM 872  '
#######################################################################################################

namespaces = functions.namespaces
sDivider = functions.sDivider
"""
            <oub:measure.sid>3639381</oub:measure.sid>
            <oub:footnote.type.id>TM</oub:footnote.type.id>
            <oub:footnote.id>872</oub:footnote.id>
"""
def convert(root):
	global namespaces
	global sDivider

	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:footnote.association.measure/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:footnote.association.measure/oub:measure.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:footnote.association.measure/oub:footnote.type.id", 2, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:footnote.association.measure/oub:footnote.id", 4, " ", functions.datatype.string)
		sOut += "  '\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
	