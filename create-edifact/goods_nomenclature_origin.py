import functions

#######################################################################################################
# GET GOODS NOMENCLATURE ORIGINS
"""
        <xs:element name="goods.nomenclature.sid" type="SID"/>
        <xs:element name="derived.goods.nomenclature.item.id" type="GoodsNomenclatureItemId"/>
        <xs:element name="derived.productline.suffix" type="ProductLineSuffix"/>
        <xs:element name="goods.nomenclature.item.id" type="GoodsNomenclatureItemId"/>
        <xs:element name="productline.suffix" type="ProductLineSuffix"/>
"""
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:goods.nomenclature.origin/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider
		
		sOut += functions.edi(oNode, "oub:goods.nomenclature.origin/oub:goods.nomenclature.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:goods.nomenclature.origin/oub:derived.goods.nomenclature.item.id", 10, "0", functions.datatype.string, "left") + functions.sDivider
		sOut += functions.edi(oNode, "oub:goods.nomenclature.origin/oub:derived.productline.suffix", 2, "0", functions.datatype.string, "left") + functions.sDivider
		sOut += functions.edi(oNode, "oub:goods.nomenclature.origin/oub:goods.nomenclature.item.id", 10, "0", functions.datatype.string, "left") + functions.sDivider
		sOut += functions.edi(oNode, "oub:goods.nomenclature.origin/oub:productline.suffix", 2, "0", functions.datatype.string, "left") + functions.sDivider
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
