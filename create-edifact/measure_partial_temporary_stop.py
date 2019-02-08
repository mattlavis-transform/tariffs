import functions

#######################################################################################################
# MEASURE PARTIAL TEMPORARY STOP
"""
  <xs:element name="measure.partial.temporary.stop" substitutionGroup="abstract.record">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="measure.sid" type="SID"/>
        <xs:element name="validity.start.date" type="Date"/>
        <xs:element name="validity.end.date" type="Date" minOccurs="0"/>
        <xs:element name="partial.temporary.stop.regulation.id" type="RegulationId"/>
        <xs:element name="partial.temporary.stop.regulation.officialjournal.number" type="OfficialJournalNumber" minOccurs="0"/>
        <xs:element name="partial.temporary.stop.regulation.officialjournal.page" type="OfficialJournalPage" minOccurs="0"/>
        <xs:element name="abrogation.regulation.id" type="RegulationId" minOccurs="0"/>
        <xs:element name="abrogation.regulation.officialjournal.number" type="OfficialJournalNumber" minOccurs="0"/>
        <xs:element name="abrogation.regulation.officialjournal.page" type="OfficialJournalPage" minOccurs="0"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
"""
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//measure.partial.temporary.stop/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider

		sOut += functions.edi(oNode, "oub:measure.partial.temporary.stop/oub:measure.sid",                                               8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.partial.temporary.stop/oub:validity.start.date",                                       8, "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.partial.temporary.stop/oub:validity.end.date",                                         8, "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.partial.temporary.stop/oub:partial.temporary.stop.regulation.id",                      8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.partial.temporary.stop/oub:partial.temporary.stop.regulation.officialjournal.number",  5, " ", functions.datatype.string, "left") + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.partial.temporary.stop/oub:partial.temporary.stop.regulation.officialjournal.page",    4, " ", functions.datatype.string, "left") + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.partial.temporary.stop/oub:abrogation.regulation.id",                                  8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.partial.temporary.stop/oub:abrogation.regulation.officialjournal.number",              5, " ", functions.datatype.string, "left") + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.partial.temporary.stop/oub:abrogation.regulation.officialjournal.page",                4, " ", functions.datatype.string, "left") + functions.sDivider
		sOut += "  '\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
