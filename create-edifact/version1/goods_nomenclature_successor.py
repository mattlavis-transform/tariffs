import functions

#######################################################################################################
# GET GOODS NOMENCLATURE SUCCESSORS
"""
        <xs:element name="goods.nomenclature.sid" type="SID"/>
        <xs:element name="absorbed.goods.nomenclature.item.id" type="GoodsNomenclatureItemId"/>
        <xs:element name="absorbed.productline.suffix" type="ProductLineSuffix"/>
        <xs:element name="goods.nomenclature.item.id" type="GoodsNomenclatureItemId"/>
        <xs:element name="productline.suffix" type="ProductLineSuffix"/>
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
	for oNode in root.findall('.//oub:goods.nomenclature.successor/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)
		
		sOut += functions.edi(oNode, "oub:goods.nomenclature.successor/oub:goods.nomenclature.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:goods.nomenclature.successor/oub:absorbed.goods.nomenclature.item.id", 10, "0", functions.datatype.string, "left")
		sOut += functions.edi(oNode, "oub:goods.nomenclature.successor/oub:absorbed.productline.suffix", 2, "0", functions.datatype.string, "left")
		sOut += functions.edi(oNode, "oub:goods.nomenclature.successor/oub:goods.nomenclature.item.id", 10, "0", functions.datatype.string, "left")
		sOut += functions.edi(oNode, "oub:goods.nomenclature.successor/oub:productline.suffix", 2, "0", functions.datatype.string, "left")
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)