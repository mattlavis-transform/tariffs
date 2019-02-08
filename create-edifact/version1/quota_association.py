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

namespaces = functions.namespaces
sDivider = functions.sDivider

def convert(root):
	global namespaces
	global sDivider

	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:quota.association/../../oub:record', namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

		sOut += functions.edi(oNode, "oub:quota.association/oub:main.quota.definition.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.association/oub:sub.quota.definition.sid", 8, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.association/oub:relation.type", 3, "0", functions.datatype.string)
		sOut += functions.edi(oNode, "oub:quota.association/oub:coefficient", 17, "0", functions.datatype.string)
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
	
