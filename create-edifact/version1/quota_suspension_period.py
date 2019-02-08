import functions

#######################################################################################################
# GET QUOTA DEFINITIONS
"""
        <xs:element name="quota.suspension.period.sid" type="SID"/>
        <xs:element name="quota.definition.sid" type="SID"/>
        <xs:element name="suspension.start.date" type="Date"/>
        <xs:element name="suspension.end.date" type="Date"/>
        <xs:element name="description" type="ShortDescription" minOccurs="0"/>
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
	for oNode in root.findall('.//oub:quota.closed.and.transferred.event/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:quota.closed.and.transferred.event/oub:quota.suspension.period.sid", 8,  "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.closed.and.transferred.event/oub:quota.definition.sid",        8,  "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.closed.and.transferred.event/oub:suspension.start.date",       8,  "0", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:quota.closed.and.transferred.event/oub:suspension.end.date",         8,  "0", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:quota.closed.and.transferred.event/oub:description",                 -1, " ", functions.datatype.string)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
	
