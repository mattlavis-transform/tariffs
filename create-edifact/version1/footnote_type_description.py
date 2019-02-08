import functions

#######################################################################################################
# GET FOOTNOTE TYPE DESCRIPTION
"""
        <xs:element name="footnote.type.id" type="FootnoteTypeId"/>
        <xs:element name="language.id" type="LanguageId"/>
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
	for oNode in root.findall('.//oub:footnote.type.description/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:footnote.type.description/oub:footnote.type.id", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:footnote.type.description/oub:language.id", 2, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:footnote.type.description/oub:description", -1, "0", functions.datatype.string)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)