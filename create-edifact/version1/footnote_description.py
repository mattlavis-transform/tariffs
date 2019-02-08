import functions

#######################################################################################################
# GET FOOTNOTE DESCRIPTIONS
"""
        <xs:element name="footnote.description.period.sid" type="SID"/>
        <xs:element name="language.id" type="LanguageId"/>
        <xs:element name="footnote.type.id" type="FootnoteTypeId"/>
        <xs:element name="footnote.id" type="FootnoteId"/>
        <xs:element name="description" type="LongDescription" minOccurs="0"/>
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
	for oNode in root.findall('.//oub:footnote.description/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)
		
		sOut += functions.edi(oNode, "oub:footnote.description/oub:footnote.description.period.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:footnote.description/oub:language.id", 2, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:footnote.description/oub:footnote.type.id", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:footnote.description/oub:footnote.id", 5, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:footnote.description/oub:description", -1, "0", functions.datatype.string)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)