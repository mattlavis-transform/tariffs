# Import external libraries
import xml.etree.ElementTree as ET
import csv
import sys
import datetime

# Import custom libraries
import functions

import additional_code_type
import additional_code_type_description
import additional_code_type_measure_type
import additional_code
import additional_code_description_period
import additional_code_description

import base_regulation

import certificate_type
import certificate_type_description
import certificate
import certificate_description_period
import certificate_description

import footnote_type
import footnote_type_description
import footnote
import footnote_description_period
import footnote_description

import geographical_area
import geographical_area_description_period
import geographical_area_description
import geographical_area_membership

import goods_nomenclature
import goods_nomenclature_indents
import goods_nomenclature_description_period
import goods_nomenclature_description
import goods_nomenclature_origin
import goods_nomenclature_successor

import measure
import measure_condition
import measure_condition_component

import footnote_association_measure
import measure_component
import measure_excluded_geographical_area

import quota_order_number
import quota_order_number_origin
import quota_order_number_origin_exclusions
import quota_definition
import quota_association

import quota_closed_and_transferred_event
import quota_suspension_period
import quota_unsuspension_event

import regulation_group
import regulation_group_description

# Global variables
namespaces = functions.namespaces
sDivider = functions.sDivider

# Load file
tree = ET.parse("../xml/TGB18109_orig.xml")
root = tree.getroot()

# open a file for writing
oEdifact = open('../edifact/Matt_TGB18109.txt', 'w')

# Get the date and time for the header and footer
now = datetime.datetime.now()
sDate = str(now.day).zfill(2)
sDate += str(now.month).zfill(2)
sDate += str(now.year).zfill(4)
sDate += ":"
sDate += str(now.hour).zfill(2)
sDate += str(now.minute).zfill(2)

# Get the envelope details
sIdentifier = root.attrib["id"]

# Write the header
oEdifact.write("UNB+XXIB:1+CEC/XXI/B5+               GB+" + sDate + "+TARIC'\n")
oEdifact.write("UNH+TGBGB" + sIdentifier + "+" + sIdentifier[1:] + "'\n")
functions.iCount = 3
functions.dictRecordCount = {}
functions.dictSequence = {}

iCount = 0
for oNode in root.findall('.//oub:record', namespaces):
	iCount += 1
	sOut = ""
	sOut += functions.edi(oNode, "oub:transaction.id", 10, "0", functions.datatype.string)
	sRecordCode = functions.edi(oNode, "oub:record.code", 3, "0", functions.datatype.string)
	sSubRecordCode = functions.edi(oNode, "oub:subrecord.code", 2, "0", functions.datatype.string)

	sOut += sRecordCode
	sOut += sSubRecordCode

	sOut += "+"
	sOut += functions.edi(oNode, "oub:record.sequence.number", 8, "0", functions.datatype.string)
	sOut += functions.edi(oNode, "oub:update.type", 1, "0", functions.datatype.string)

	oNode2 = oNode[5]
	sTag = oNode2.tag.replace("{urn:publicid:-:DGTAXUD:TARIC:MESSAGE:1.0}", "")
	# print(sTag)
	if (sTag == "additional.code"):
		sOut += additional_code.convert2(oNode2)
	elif (sTag == "additional.code.description"):
		sOut += additional_code_description.convert2(oNode2)
	elif (sTag == "additional.code.description.period"):
		sOut += additional_code_description_period.convert2(oNode2)
	elif (sTag == "additional.code.type"):
		sOut += additional_code_type.convert2(oNode2)
	elif (sTag == "additional.code.type.description"):
		sOut += additional_code_type_description.convert2(oNode2)
	elif (sTag == "additional.code.type.measure.type"):
		sOut += additional_code_type_measure_type.convert2(oNode2)
	elif (sTag == "base.regulation"):
		sOut += base_regulation.convert2(oNode2)
	elif (sTag == "certificate"):
		sOut += certificate.convert2(oNode2)
	elif (sTag == "certificate.description"):
		sOut += certificate_description.convert2(oNode2)
	elif (sTag == "certificate.description.period"):
		sOut += certificate_description_period.convert2(oNode2)
	elif (sTag == "certificate.type"):
		sOut += certificate_type.convert2(oNode2)
	elif (sTag == "certificate.type.description"):
		sOut += certificate_type_description.convert2(oNode2)
	elif (sTag == "footnote"):
		sOut += footnote.convert2(oNode2)
	elif (sTag == "footnote.association.measure"):
		sOut += footnote_association_measure.convert2(oNode2)
	elif (sTag == "footnote.description"):
		sOut += footnote_description.convert2(oNode2)
	elif (sTag == "footnote.description.period"):
		sOut += footnote_description_period.convert2(oNode2)
	elif (sTag == "footnote.type"):
		sOut += footnote_type.convert2(oNode2)
	elif (sTag == "footnote.type.description"):
		sOut += footnote_type_description.convert2(oNode2)
	elif (sTag == "geographical.area"):
		sOut += geographical_area.convert2(oNode2)
	elif (sTag == "geographical.area.description"):
		sOut += geographical_area_description.convert2(oNode2)
	elif (sTag == "geographical.area.description.period"):
		sOut += geographical_area_description_period.convert2(oNode2)
	elif (sTag == "geographical.area.membership"):
		sOut += geographical_area_membership.convert2(oNode2)
	elif (sTag == "goods.nomenclature"):
		sOut += goods_nomenclature.convert2(oNode2)
	elif (sTag == "goods.nomenclature.description"):
		sOut += goods_nomenclature_description.convert2(oNode2)
	elif (sTag == "goods.nomenclature.description.period"):
		sOut += goods_nomenclature_description_period.convert2(oNode2)
	elif (sTag == "goods.nomenclature.indents"):
		sOut += goods_nomenclature_indents.convert2(oNode2)
	elif (sTag == "goods.nomenclature.origin"):
		sOut += goods_nomenclature_origin.convert2(oNode2)
	elif (sTag == "goods.nomenclature.successor"):
		sOut += goods_nomenclature_successor.convert2(oNode2)
	elif (sTag == "measure"):
		sOut += measure.convert2(oNode2)
	elif (sTag == "measure.component"):
		sOut += measure_component.convert2(oNode2)
	elif (sTag == "measure.condition"):
		sOut += measure_condition.convert2(oNode2)
	elif (sTag == "measure.condition.component"):
		sOut += measure_condition_component.convert2(oNode2)
	elif (sTag == "measure.excluded.geographical.area"):
		sOut += measure_excluded_geographical_area.convert2(oNode2)
	elif (sTag == "quota.association"):
		sOut += quota_association.convert2(oNode2)
	elif (sTag == "quota.closed.and.transferred.event"):
		sOut += quota_closed_and_transferred_event.convert2(oNode2)
	elif (sTag == "quota.definition"):
		sOut += quota_definition.convert2(oNode2)
	elif (sTag == "quota.order.number"):
		sOut += quota_order_number.convert2(oNode2)
	elif (sTag == "quota.order.number.origin"):
		sOut += quota_order_number_origin.convert2(oNode2)
	elif (sTag == "quota.order.number.origin.exclusions"):
		sOut += quota_order_number_origin_exclusions.convert2(oNode2)
	elif (sTag == "quota.suspension.period"):
		sOut += quota_suspension_period.convert2(oNode2)
	elif (sTag == "quota.unsuspension.event"):
		sOut += quota_unsuspension_event.convert2(oNode2)
	elif (sTag == "regulation.group"):
		sOut += regulation_group.convert2(oNode2)
	elif (sTag == "regulation.group.description"):
		sOut += regulation_group_description.convert2(oNode2)

	sOut += "'\n"
	oEdifact.write(sOut)


# Write the special control record
sRecordCounts = ""
for k in functions.dictRecordCount:
	sRecordCounts += k + str(functions.dictRecordCount[k]).zfill(8)

oEdifact.write("999+" + str(iCount - 1).zfill(8) + "+" + sRecordCounts + "'\n")


# Write the footer
oEdifact.write("UNT+" + str(iCount).zfill(8) + "+TGBGB" + sIdentifier + "'\n")
oEdifact.write("UNZ+01+TARIC'\n")

# close the file object
oEdifact.close()
