import functions

#######################################################################################################
# GET QUOTA ORDER NUMBER ORIGINS
"""
        <xs:element name="quota.order.number.origin.sid" type="SID"/>
        <xs:element name="quota.order.number.sid" type="SID"/>
        <xs:element name="geographical.area.id" type="GeographicalAreaId"/>
        <xs:element name="validity.start.date" type="Date"/>
        <xs:element name="validity.end.date" type="Date" minOccurs="0"/>
        <xs:element name="geographical.area.sid" type="SID"/>
"""
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:quota.order.number.origin/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider

		sOut += functions.edi(oNode, "oub:quota.order.number.origin/oub:quota.order.number.origin.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:quota.order.number.origin/oub:quota.order.number.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:quota.order.number.origin/oub:geographical.area.id", 4, "0", functions.datatype.string, "left") + functions.sDivider
		sOut += functions.edi(oNode, "oub:quota.order.number.origin/oub:validity.start.date", 8, " ", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:quota.order.number.origin/oub:validity.end.date", 8, "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:quota.order.number.origin/oub:geographical.area.sid", 8, "0", functions.datatype.string, "left") + functions.sDivider
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
