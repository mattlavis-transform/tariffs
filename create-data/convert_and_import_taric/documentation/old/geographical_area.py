import functions

#######################################################################################################
# GET GEOGRAPHICAL AREA TYPE
"""
        <xs:element name="geographical.area.sid" type="SID"/>
        <xs:element name="geographical.area.id" type="GeographicalAreaId"/>
        <xs:element name="validity.start.date" type="Date"/>
        <xs:element name="validity.end.date" type="Date" minOccurs="0"/>
        <xs:element name="geographical.code" type="AreaCode"/>
        <xs:element name="parent.geographical.area.group.sid" type="SID" minOccurs="0"/>
"""
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:geographical.area/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider

		sOut += functions.edi(oNode, "oub:geographical.area/oub:geographical.area.sid", 1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:geographical.area/oub:geographical.area.id", 4, "0", functions.datatype.string, "left") + functions.sDivider
		sOut += functions.edi(oNode, "oub:geographical.area/oub:validity.start.date", 8, "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:geographical.area/oub:geographical.code", 1, "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:geographical.area/oub:geographical.area.group.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
