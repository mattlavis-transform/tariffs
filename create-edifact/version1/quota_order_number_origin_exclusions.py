import functions

#######################################################################################################
# GET QUOTA ORDER NUMBER ORIGIN EXCLUSIONS
"""
        <xs:element name="quota.order.number.origin.sid" type="SID"/>
        <xs:element name="excluded.geographical.area.sid" type="SID"/>
"""
#######################################################################################################

namespaces = functions.namespaces
sDivider = functions.sDivider

def convert(root):
	global namespaces
	global sDivider

	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:quota.order.number.origin.exclusions/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:quota.order.number.origin.exclusions/oub:quota.order.number.origin.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.order.number.origin.exclusions/oub:excluded.geographical.area.sid", 8, "0", functions.datatype.string)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
	
