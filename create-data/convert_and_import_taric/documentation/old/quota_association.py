import functions

#######################################################################################################
# GET QUOTA ASSOCIATIONS
"""
        <xs:element name="main.quota.definition.sid" type="SID"/>
        <xs:element name="sub.quota.definition.sid" type="SID"/>
        <xs:element name="relation.type" type="RelationType"/>
        <xs:element name="coefficient" type="QuotaCoefficient" minOccurs="0"/>
"""
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:quota.association/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider

		sOut += functions.edi(oNode, "oub:quota.association/oub:main.quota.definition.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:quota.association/oub:sub.quota.definition.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:quota.association/oub:relation.type", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:quota.association/oub:coefficient", 17, "0", functions.datatype.string) + functions.sDivider
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
