import functions

#######################################################################################################
# GET MEASURE TYPE
"""
        <xs:element name="measure.type.id" type="MeasureTypeId"/>
        <xs:element name="validity.start.date" type="Date"/>
        <xs:element name="validity.end.date" type="Date" minOccurs="0"/>
        <xs:element name="trade.movement.code" type="TradeMovementCode"/>
        <xs:element name="priority.code" type="PriorityCode"/>
        <xs:element name="measure.component.applicable.code" type="MeasurementUnitApplicabilityCode"/>
        <xs:element name="origin.dest.code" type="OriginCode"/>
        <xs:element name="order.number.capture.code" type="OrderNumberCaptureCode"/>
        <xs:element name="measure.explosion.level" type="MeasureExplosionLevel"/>
        <xs:element name="measure.type.series.id" type="MeasureTypeSeriesId"/>

"""
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:measure.type/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "./oub:measure.type.id",                   6, " ", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "./oub:validity.start.date",               8, "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "./oub:validity.end.date",                 8, "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "./oub:trade.movement.code",               1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "./oub:priority.code",                     1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "./oub:measure.component.applicable.code", 1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "./oub:origin.dest.code",                  1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "./oub:order.number.capture.code",         1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "./oub:measure.explosion.level",           2, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "./oub:measure.type.series.id",            2, "0", functions.datatype.string) + functions.sDivider
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
