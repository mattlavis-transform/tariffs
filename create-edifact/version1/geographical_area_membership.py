import functions

#######################################################################################################
# GET GEOGRAPHICAL AREA MEMBERSHIP
"""
        <xs:element name="geographical.area.sid" type="SID"/>
        <xs:element name="geographical.area.group.sid" type="SID"/>
        <xs:element name="validity.start.date" type="Date"/>
        <xs:element name="validity.end.date" type="Date" minOccurs="0"/>
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
	for oNode in root.findall('.//oub:geographical.area.membership/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:geographical.area.membership/oub:geographical.area.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:geographical.area.membership/oub:geographical.area.group.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:geographical.area.membership/oub:validity.start.date", 8, "0", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:geographical.area.membership/oub:validity.end.date", 8, "0", functions.datatype.date)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)