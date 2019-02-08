import functions

#######################################################################################################
# GET GOODS NOMENCLATURE
"""
        <xs:element name="goods.nomenclature.sid" type="SID"/>
        <xs:element name="goods.nomenclature.item.id" type="GoodsNomenclatureItemId"/>
        <xs:element name="producline.suffix" type="ProductLineSuffix"/>
        <xs:element name="validity.start.date" type="Date"/>
        <xs:element name="validity.end.date" type="Date" minOccurs="0"/>
        <xs:element name="statistical.indicator" type="StatisticalIndicator"/>
"""
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:goods.nomenclature/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider

		sOut += functions.edi(oNode, "oub:goods.nomenclature/oub:goods.nomenclature.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:goods.nomenclature/oub:goods.nomenclature.item.id", 10, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:goods.nomenclature/oub:producline.suffix", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:goods.nomenclature/oub:validity.start.date", 8, "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:goods.nomenclature/oub:validity.end.date", 8, "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:goods.nomenclature/oub:statistical.indicator", 1, "0", functions.datatype.string) + functions.sDivider
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)