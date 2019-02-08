import functions

#######################################################################################################
# GET CERTIFICATE DESCRIPTIONS
"""
        <xs:element name="certificate.description.period.sid" type="SID"/>
        <xs:element name="language.id" type="LanguageId"/>
        <xs:element name="certificate.type.code" type="CertificateTypeCode"/>
        <xs:element name="certificate.code" type="CertificateCode"/>
        <xs:element name="description" type="ShortDescription" minOccurs="0"/>
"""
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:certificate.description/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider
		
		sOut += functions.edi(oNode, "oub:certificate.description/oub:certificate.description.period.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:certificate.description/oub:language.id", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:certificate.description/oub:certificate.type.code", 1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:certificate.description/oub:certificate.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:certificate.description/oub:description", -1, "0", functions.datatype.string) + functions.sDivider
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
