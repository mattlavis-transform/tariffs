import functions

#######################################################################################################
# GET ADDITIONAL CODE DESCRIPTIONS
# 001604202024510+00000002300009728EN00012351B922Suzhou Talesun Solar Technologies Co.<P>Ltd'
#######################################################################################################

def convert(root):
	sOut = ""
	sRecordCode = ""
	iLocal = 0
	for oNode in root.findall('.//oub:additional.code.description/../../oub:record', functions.namespaces):
		functions.iCount += 1
		iLocal += 1
		sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string) + functions.sDivider
		sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string) + functions.sDivider
		sOut += sRecordCode
		sOut += functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string) + functions.sDivider
		sOut += "+"
		sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:additional.code.description/oub:additional.code.description.period.sid", 8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:additional.code.description/oub:language.id",                            2, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:additional.code.description/oub:additional.code.sid",                    8, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:additional.code.description/oub:additional.code.type.id",                1, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:additional.code.description/oub:additional.code",                        3, "0", functions.datatype.string) + functions.sDivider
		sOut += functions.edi(oNode, "oub:additional.code.description/oub:description",                           -1, "0", functions.datatype.string) + functions.sDivider
		sOut += "'\n"

	functions.updateRecordCount(sRecordCode, iLocal)
	return (sOut)
