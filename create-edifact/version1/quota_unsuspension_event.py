import functions

#######################################################################################################
# GET QUOTA DEFINITIONS
"""
        <xs:element name="quota.definition.sid" type="SID"/>
        <xs:element name="occurrence.timestamp" type="Timestamp"/>
        <xs:element name="unsuspension.date" type="Date"/>
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
	for oNode in root.findall('.//oub:quota.unsuspension.event/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:quota.unsuspension.event/oub:quota.definition.sid", 8,  "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.unsuspension.event/oub:occurrence.timestamp", 8,  "0", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:quota.unsuspension.event/oub:unsuspension.date",    8,  "0", functions.datatype.date)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
	
