import functions

#######################################################################################################
# GET CERTIFICATE DESCRIPTION PERIODS
"""
        <xs:element name="certificate.description.period.sid" type="SID"/>
        <xs:element name="certificate.type.code" type="CertificateTypeCode"/>
        <xs:element name="certificate.code" type="CertificateCode"/>
        <xs:element name="validity.start.date" type="Date"/>
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
	for oNode in root.findall('.//oub:certificate.description.period/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)
		
		sOut += functions.edi(oNode, "oub:certificate.description.period/oub:certificate.description.period.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:certificate.description.period/oub:certificate.type.code", 1, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:certificate.description.period/oub:certificate.code", 3, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:certificate.description.period/oub:validity.start.date", 8, "0", functions.datatype.date)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)