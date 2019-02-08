import functions

#######################################################################################################
# GET QUOTA DEFINITIONS
"""
        <xs:element name="quota.definition.sid" type="SID"/>
        <xs:element name="occurrence.timestamp" type="Timestamp"/>
        <xs:element name="unsuspension.date" type="Date"/>
"""
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:quota.unsuspension.event/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider

		sOut += functions.edi(oNode, "oub:quota.unsuspension.event/oub:quota.definition.sid", 8,  "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:quota.unsuspension.event/oub:occurrence.timestamp", 8,  "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:quota.unsuspension.event/oub:unsuspension.date",    8,  "0", functions.datatype.date) + functions.sDivider
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
