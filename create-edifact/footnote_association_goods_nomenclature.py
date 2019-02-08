import functions

#######################################################################################################
# GET FOOTNOTE ASSOCIATION GOODS NOMENCLATURE
"""
  <xs:element name="footnote.association.goods.nomenclature" substitutionGroup="abstract.record">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="goods.nomenclature.sid" type="SID"/>
        <xs:element name="footnote.type" type="FootnoteTypeId"/>
        <xs:element name="footnote.id" type="FootnoteId"/>
        <xs:element name="validity.start.date" type="Date"/>
        <xs:element name="validity.end.date" type="Date" minOccurs="0"/>
        <xs:element name="goods.nomenclature.item.id" type="GoodsNomenclatureItemId"/>
        <xs:element name="productline.suffix" type="ProductLineSuffix"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
"""
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:footnote.association.goods.nomenclature/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider

		sOut += functions.edi(oNode, "oub:footnote.association.goods.nomenclature/oub:goods.nomenclature.sid",      8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:footnote.association.goods.nomenclature/oub:footnote.type",               3, " ", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:footnote.association.goods.nomenclature/oub:footnote.id",                 5, " ", functions.datatype.string, "left") + functions.sDivider
		sOut += functions.edi(oNode, "oub:footnote.association.goods.nomenclature/oub:validity.start.date",         8, "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:footnote.association.goods.nomenclature/oub:validity.end.date",           8, "0", functions.datatype.date) + functions.sDivider
		sOut += functions.edi(oNode, "oub:footnote.association.goods.nomenclature/oub:goods.nomenclature.item.id", 10, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:footnote.association.goods.nomenclature/oub:productline.suffix",          2, " ", functions.datatype.string) + functions.sDivider
		sOut += "  '\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
