import functions

#######################################################################################################
# GET MEASURE CONDITIONS
"""
        <xs:element name="measure.condition.sid" type="SID"/>
        <xs:element name="measure.sid" type="SID"/>
        <xs:element name="condition.code" type="ConditionCode"/>
        <xs:element name="component.sequence.number" type="ComponentSequenceNumber"/>
        <xs:element name="condition.duty.amount" type="DutyAmount" minOccurs="0"/>
        <xs:element name="condition.monetary.unit.code" type="MonetaryUnitCode" minOccurs="0"/>
        <xs:element name="condition.measurement.unit.code" type="MeasurementUnitCode" minOccurs="0"/>
        <xs:element name="condition.measurement.unit.qualifier.code" type="MeasurementUnitQualifierCode" minOccurs="0"/>
        <xs:element name="action.code" type="ActionCode" minOccurs="0"/>
        <xs:element name="certificate.type.code" type="CertificateTypeCode" minOccurs="0"/>
        <xs:element name="certificate.code" type="CertificateCode" minOccurs="0"/>
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
	for oNode in root.findall('.//oub:measure.condition/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:measure.condition/oub:measure.condition.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure.condition/oub:measure.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure.condition/oub:measure.condition.code", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure.condition/oub:component.sequence.number", 3, " ", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure.condition/oub:condition.duty.amount", 10, " ", functions.datatype.currency)
		sOut += functions.edi(oNode, "oub:measure.condition/oub:condition.monetary.unit.code", 3, " ", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure.condition/oub:condition.measurement.unit.code", 3, " ", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure.condition/oub:condition.measurement.unit.qualifier.code", 1, " ", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure.condition/oub:action.code", 1, " ", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure.condition/oub:certificate.type.code", 1, " ", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:measure.condition/oub:certificate.code", 3, " ", functions.datatype.string)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
	
