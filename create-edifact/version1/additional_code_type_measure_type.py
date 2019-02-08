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

namespaces = functions.namespaces
sDivider = functions.sDivider

def convert(root):
	global namespaces
	global sDivider

	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:additional.code.type.measure.type/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:additional.code.type.measure.type/oub:additional.measure.type.id", 6, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:additional.code.type.measure.type/oub:additional.code.type.id", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:additional.code.type.measure.type/oub:validity.start.date", 8, "0", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:additional.code.type.measure.type/oub:validity.end.date", 8, "0", functions.datatype.date)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)