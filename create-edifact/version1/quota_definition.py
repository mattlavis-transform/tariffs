import functions

#######################################################################################################
# GET QUOTA DEFINITIONS
"""
        <xs:element name="quota.definition.sid" type="SID"/>
        <xs:element name="quota.order.number.id" type="OrderNumber"/>
        <xs:element name="validity.start.date" type="Date"/>
        <xs:element name="validity.end.date" type="Date" minOccurs="0"/>
        <xs:element name="quota.order.number.sid" type="SID"/>
        <xs:element name="volume" type="QuotaAmount"/>
        <xs:element name="initial.volume" type="QuotaAmount"/>
        <xs:element name="monetary.unit.code" type="MonetaryUnitCode" minOccurs="0"/>
        <xs:element name="measurement.unit.code" type="MeasurementUnitCode" minOccurs="0"/>
        <xs:element name="measurement.unit.qualifier.code" type="MeasurementUnitQualifierCode" minOccurs="0"/>
        <xs:element name="maximum.precision" type="QuotaPrecision"/>
        <xs:element name="critical.state" type="QuotaCriticalStateCode"/>
        <xs:element name="critical.threshold" type="QuotaCriticalTreshold"/>
        <xs:element name="description" type="ShortDescription" minOccurs="0"/>
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
	for oNode in root.findall('.//oub:quota.definition/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:quota.definition/oub:quota.definition.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.definition/oub:quota.order.number.id", 6, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.definition/oub:validity.start.date", 8, " ", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:quota.definition/oub:validity.end.date", 8, "0", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:quota.definition/oub:quota.order.number.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.definition/oub:volume", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.definition/oub:initial.volume", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.definition/oub:monetary.unit.code", 3, " ", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.definition/oub:measurement.unit.code", 3, " ", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.definition/oub:measurement.unit.qualifier.code", 1, " ", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.definition/oub:maximum.precision", 1, " ", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.definition/oub:critical.state", 1, " ", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.definition/oub:critical.threshold", 8, " ", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.definition/oub:description", -1, " ", functions.datatype.string)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
	
