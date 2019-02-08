import functions

#######################################################################################################
# GET GOODS NOMENCLATURE INDENTS
"""
        <xs:element name="goods.nomenclature.indents.indent.sid" type="SID"/>
        <xs:element name="goods.nomenclature.indents.sid" type="SID"/>
        <xs:element name="validity.start.date" type="Date"/>
        <xs:element name="number.indents" type="NumberOf"/>
        <xs:element name="goods.nomenclature.indents.item.id" type="GoodsNomenclatureItemId"/>
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
	for oNode in root.findall('.//oub:goods.nomenclature.indents/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:goods.nomenclature.indents/oub:goods.nomenclature.indents.indent.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:goods.nomenclature.indents/oub:goods.nomenclature.indents.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:goods.nomenclature.indents/oub:validity.start.date", 8, "0", functions.datatype.date)
		sOut += functions.edi(oNode, "oub:goods.nomenclature.indents/oub:goods.nomenclature.indents.item.id", 10, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:goods.nomenclature.indents/oub:productline.suffix", 2, "0", functions.datatype.string)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)