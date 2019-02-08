import functions

#######################################################################################################
# GET GEOGRAPHICAL AREA DESCRIPTION PERIODS
"""
        <xs:element name="geographical.area.description.period.sid" type="SID"/>
        <xs:element name="geographical.area.sid" type="SID"/>
        <xs:element name="validity.start.date" type="Date"/>
        <xs:element name="geographical.area.id" type="GeographicalAreaId"/>
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
	for oNode in root.findall('.//oub:geographical.area.description.period/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)
		
		sOut += functions.edi(oNode, "oub:geographical.area.description.period/oub:geographical.area.description.period.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:geographical.area.description.period/oub:geographical.area.sid", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:geographical.area.description.period/oub:validity.start.date", 8, "0", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:geographical.area.description.period/oub:geographical.area.id", 4, "0", functions.datatype.string, "left")
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)