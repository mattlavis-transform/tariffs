import functions

#######################################################################################################
# GET ADDITIONAL CODE TYPE MEASURE TYPE
"""
        <xs:element name="measure.type.id" type="MeasureTypeId"/>
        <xs:element name="additional.code.type.id" type="AdditionalCodeTypeId"/>
        <xs:element name="validity.start.date" type="Date"/>
        <xs:element name="validity.end.date" type="Date" minOccurs="0"/>
"""
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:additional.code.type.measure.type/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider

		sOut += functions.edi(oNode, "oub:additional.code.type.measure.type/oub:additional.measure.type.id", 6, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:additional.code.type.measure.type/oub:additional.code.type.id", 1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:additional.code.type.measure.type/oub:validity.start.date", 8, "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:additional.code.type.measure.type/oub:validity.end.date", 8, "0", functions.datatype.date) + functions.sDivider
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
