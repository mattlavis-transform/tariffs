import functions

#######################################################################################################
# GET BASE REGULATIONS
"""
        <xs:element name="base.regulation.role" type="RegulationRoleTypeId"/>
        <xs:element name="base.regulation.id" type="RegulationId"/>
        <xs:element name="published.date" type="Date" minOccurs="0"/>
        <xs:element name="officialjournal.number" type="OfficialJournalNumber" minOccurs="0"/>
        <xs:element name="officialjournal.page" type="OfficialJournalPage" minOccurs="0"/>
        <xs:element name="validity.start.date" type="Date"/>
        <xs:element name="validity.end.date" type="Date" minOccurs="0"/>
        <xs:element name="effective.end.date" type="Date" minOccurs="0"/>
        <xs:element name="community.code" type="CommunityCode"/>
        <xs:element name="regulation.group.id" type="RegulationGroupId"/>
        <xs:element name="antidumping.regulation.role" type="RegulationRoleTypeId" minOccurs="0"/>
        <xs:element name="related.antidumping.regulation.id" type="RegulationId" minOccurs="0"/>
        <xs:element name="complete.abrogation.regulation.role" type="RegulationRoleTypeId" minOccurs="0"/>
        <xs:element name="complete.abrogation.regulation.id" type="RegulationId" minOccurs="0"/>
        <xs:element name="explicit.abrogation.regulation.role" type="RegulationRoleTypeId" minOccurs="0"/>
        <xs:element name="explicit.abrogation.regulation.id" type="RegulationId" minOccurs="0"/>
        <xs:element name="replacement.indicator" type="ReplacementIndicator"/>
        <xs:element name="stopped.flag" type="StoppedFlag"/>
        <xs:element name="information.text" type="ShortDescription" minOccurs="0"/>
        <xs:element name="approved.flag" type="ApprovedFlag"/>
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
	for oNode in root.findall('.//oub:base.regulation/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:base.regulation/oub:base.regulation.role", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:base.regulation.id", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:published.date", 8, " ", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:officialjournal.number", 5, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:officialjournal.page", 4, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:validity.start.date", 8, "0", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:validity.end.date", 8, "0", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:effective.end.date", 8, "0", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:community.code", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:regulation.group.id", 3, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:antidumping.regulation.role", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:related.antidumping.regulation.id", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:complete.abrogation.regulation.role", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:complete.abrogation.regulation.id", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:explicit.abrogation.regulation.role", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:explicit.abrogation.regulation.id", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:replacement.indicator", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:stopped.flag", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:information.text", -1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:base.regulation/oub:approved.flag", 1, "0", functions.datatype.string)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
	
