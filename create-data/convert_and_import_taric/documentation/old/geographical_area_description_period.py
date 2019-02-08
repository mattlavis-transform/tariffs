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

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:geographical.area.description.period/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider
		
		sOut += functions.edi(oNode, "oub:geographical.area.description.period/oub:geographical.area.description.period.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:geographical.area.description.period/oub:geographical.area.sid", 1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:geographical.area.description.period/oub:validity.start.date", 8, "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:geographical.area.description.period/oub:geographical.area.id", 4, "0", functions.datatype.string, "left") + functions.sDivider
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
