import functions

#######################################################################################################
# GET FOOTNOTE ASSOCIATION MEASURE
# 001604275643020+00000028303639381TM 872  '
#######################################################################################################

namespaces = functions.namespaces
sDivider = functions.sDivider
"""
            <oub:measure.sid>3639385</oub:measure.sid>
            <oub:excluded.geographical.area>AR</oub:excluded.geographical.area>
            <oub:geographical.area.sid>37</oub:geographical.area.sid>
"""
def convert(root):
	global namespaces
	global sDivider

	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:measure.excluded.geographical.area/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:measure.excluded.geographical.area/oub:measure.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure.excluded.geographical.area/oub:excluded.geographical.area", 4, " ", functions.datatype.string, "left")
		sOut += functions.edi(oNode, "oub:measure.excluded.geographical.area/oub:geographical.area.sid", 8, "0", functions.datatype.string)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
	
