import functions

#######################################################################################################
# GET MEASURE CONDITION COMPONENTS
"""
        <xs:element name="measure.condition.sid" type="SID"/>
        <xs:element name="duty.expression.id" type="DutyExpressionId"/>
        <xs:element name="duty.amount" type="DutyAmount" minOccurs="0"/>
        <xs:element name="monetary.unit.code" type="MonetaryUnitCode" minOccurs="0"/>
        <xs:element name="measurement.unit.code" type="MeasurementUnitCode" minOccurs="0"/>
        <xs:element name="measurement.unit.qualifier.code" type="MeasurementUnitQualifierCode" minOccurs="0"/>

"""
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:measure.condition.component/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider

		sOut += functions.edi(oNode, "oub:measure.condition.component/oub:measure.condition.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.condition.component/oub:duty.expression.id", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.condition.component/oub:duty.amount", 10, "0", functions.datatype.currency) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.condition.component/oub:monetary.unit.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.condition.component/oub:measurement.unit.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:measure.condition.component/oub:measurement.unit.qualifier.code", 1, "0", functions.datatype.string) + functions.sDivider
		sOut += " '\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
