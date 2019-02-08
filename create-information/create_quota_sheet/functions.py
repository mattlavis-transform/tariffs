from __future__ import with_statement
import psycopg2
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime
import os
import sys
import codecs
import re

def strNone(s):
	s = str(s)
	if s == "None":
		s = ""
	return (s)

def fltNone(s):
	if s == None:
		s = 0.00
	else:
		s = float(s)
	return (s)

def mShorten(s):
    s = s.replace("Hectokilogram",          "100kg")
    s = s.replace("Hectolitre",             "h1")
    s = s.replace("Minimum",                "MIN")
    s = s.replace("Maximum",                "MAX")
    s = s.replace("agricultural component", "EA")
    s = s.replace("  ",                     " ")
    s = s.replace(" %",                     "%")
    return (s)


def formatFootnote(s):
	sOut = ""
	a = s.split("\n")
	for ax in a:
		ax.strip()
		#print (ax)
		if len(ax) > 0:
			lChar = ascii(ax[0])
			lChar = ord(ax[0])
			if lChar == 8226:
				sStyle = "ListBulletinTable"
			else:
				sStyle = "NormalinTable"
			ax = ax.replace(chr(8226) + "\t", "")
			ax = ax.replace("  ", " ")
			sOut += "<w:p><w:pPr><w:pStyle w:val=\"" + sStyle + "\"/></w:pPr><w:r><w:t>" + ax + "</w:t></w:r></w:p>"
	return (sOut)

def fmtDate(d):
	try:
		d = datetime.strftime(d, '%d/%m/%y')
	except:
		d = ""
	return d

def fmtDate2(d):
	d = str(d)
	d = d[8:10] + "/" + d[5:7] + "/" + d[0:4]
	# d = datetime.strptime(d, '%d/%m/%y')
	return d
	
def combineDuties(sExisting, sNew, sDutyExpression, sDutyExpressionDescription):
	s = ""
	if sDutyExpression == "12":
		s = sExisting + " + EA"
	elif sDutyExpression == "21":
		s = sExisting + " + ADSZ"
	elif sDutyExpression == "27":
		s = sExisting + " + ADFM"
	elif sDutyExpression == "15":
		s = sExisting + " MIN " + sNew
	elif sDutyExpression == "17":
		s = sExisting + " MAX " + sNew
	else:
		s = sExisting + " + " + sNew
	
	#print (sDutyExpression + s + "IJOII")
	return s


def getSectionsChapters(conn):
	global rdSecChap
	sSQL = """
	SELECT LEFT(gn.goods_nomenclature_item_id, 2) as chapter, cs.section_id
	FROM chapters_sections cs, goods_nomenclatures gn
	WHERE cs.goods_nomenclature_sid = gn.goods_nomenclature_sid
	AND gn.producline_suffix = '80'
	ORDER BY 1
	"""
	cur = conn.cursor()
	cur.execute(sSQL)
	rows_sections_chapters = cur.fetchall()
	rdSecChap = []
	for rd in rows_sections_chapters:
		sChapter = rd[0]
		iSection = rd[1]
	
		rdSecChap.append([sChapter, iSection, 0])
		
	iLastSection = -1
	for r in rdSecChap:
		iSection = r[1]
		if iSection != iLastSection:
			r[2] = 1
		iLastSection = iSection

	
def getAllMeasurementUnitQualifiers(conn):
	global rows_qualifiers
	sSQL = "SELECT * FROM measurement_unit_qualifier_descriptions ORDER BY 1;"
	cur = conn.cursor()
	cur.execute(sSQL)
	rows_qualifiers = cur.fetchall()

def readTemplates(sDocumentType, sOrientation):
	global sDocumentXML, sHeading1XML, sHeading2XML, sHeading3XML, sHeading3XML, sTableXML, sTableRowXML, sFootnoteTableXML, sFootnoteTableRowXML
	global sFootnoteReferenceXML, sFootnotesXML, sFootnoteXML, sParaXML, sBulletXML, sBannerXML, sPageBreakXML
	path = "C:\\projects\\create_tariff_schedule\\xmlcomponents\\"

	# Main document templates
	if sDocumentType == "classification":
		fDocument = open(path + "document_classification.xml", "r") 
	else:
		if sOrientation == "landscape":
			fDocument = open(path + "document_schedule_landscape.xml", "r")
		else:
			fDocument = open(path + "document_schedule.xml", "r")
	sDocumentXML = fDocument.read()

	"""
	fTitle = open(path + "title.xml", "r") 
	sTitleXML = fTitle.read()
	"""

	fFootnoteTable = open(path + "table_footnote.xml", "r") 
	sFootnoteTableXML = fFootnoteTable.read()

	fFootnoteTableRow = open(path + "tablerow_footnote.xml", "r") 
	sFootnoteTableRowXML = fFootnoteTableRow.read()

	fHeading1 = open(path + "heading1.xml", "r") 
	sHeading1XML = fHeading1.read()

	fHeading2 = open(path + "heading2.xml", "r") 
	sHeading2XML = fHeading2.read()

	fHeading3 = open(path + "heading3.xml", "r") 
	sHeading3XML = fHeading3.read()

	fPara = open(path + "paragraph.xml", "r") 
	sParaXML = fPara.read()

	fBullet = open(path + "bullet.xml", "r") 
	sBulletXML = fBullet.read()

	fBanner = open(path + "banner.xml", "r") 
	sBannerXML = fBanner.read()

	fPageBreak = open(path + "pagebreak.xml", "r") 
	sPageBreakXML = fPageBreak.read()

	if (sDocumentType == "classification"):
		fTable    = open(path + "table_classification.xml", "r") 
		fTableRow = open(path + "tablerow_classification.xml", "r") 
	else:
		if sOrientation == "landscape":
			fTable    = open(path + "table_schedule_landscape.xml", "r") 
			fTableRow = open(path + "tablerow_schedule_landscape.xml", "r") 
		else:
			fTable    = open(path + "table_schedule.xml", "r") 
			fTableRow = open(path + "tablerow_schedule.xml", "r") 

	sTableXML = fTable.read()
	sTableRowXML = fTableRow.read()

	fFootnoteReference = open(path + "footnotereference.xml", "r") 
	sFootnoteReferenceXML = fFootnoteReference.read()

	# Footnote templates
	fFootnotes = open(path + "footnotes.xml", "r") 
	sFootnotesXML = fFootnotes.read()

	fFootnote = open(path + "footnote.xml", "r") 
	sFootnoteXML = fFootnote.read()

def getMeasurementUnit(s):
	if s == "ASV":
		return "% vol/hl" # 3302101000
	if s == "NAR":
		return "p/st"
	elif s == "CCT":
		return "ct/l"
	elif s == "CEN":
		return "100 p/st"
	elif s == "CTM":
		return "c/k"
	elif s == "DTN":
		return "100 kg/net"
	elif s == "GFI":
		return "gi F/S"
	elif s == "GRM":
		return "g"
	elif s == "HLT":
		return "hl" # 2209009100
	elif s == "HMT":
		return "100 m" # 3706909900
	elif s == "KGM":
		return "kg"
	elif s == "KLT":
		return "1,000 l"
	elif s == "KMA":
		return "kg met.am."
	elif s == "KNI":
		return "kg N"
	elif s == "KNS":
		return "kg H2O2"
	elif s == "KPH":
		return "kg KOH"
	elif s == "KPO":
		return "kg K2O"
	elif s == "KPP":
		return "kg P2O5"
	elif s == "KSD":
		return "kg 90 % sdt"
	elif s == "KSH":
		return "kg NaOH"
	elif s == "KUR":
		return "kg U"
	elif s == "LPA":
		return "l alc. 100%"
	elif s == "LTR":
		return "l"
	elif s == "MIL":
		return "1,000 p/st"
	elif s == "MTK":
		return "m2"
	elif s == "MTQ":
		return "m3"
	elif s == "MTR":
		return "m"
	elif s == "MWH":
		return "1,000 kWh"
	elif s == "NCL":
		return "ce/el"
	elif s == "NPR":
		return "pa"
	elif s == "TJO":
		return "TJ"
	elif s == "TNE":
		return "t" # 1005900020
		# return "1000 kg" # 1005900020
	else:
		return s

def addQual2(sSuppUnit, sQual, sQualDesc):
	if sQual == "C":
		return sQualDesc + " " + sSuppUnit
	else:
		return sSuppUnit + " " + sQualDesc		

def getQual(sQual, intention):
	sQualDesc = ""
	if sQual == "A":
		# if intention == "supplementary":
		sQualDesc = "tot/alc" # Total alcohol
	if sQual == "C":
		if intention == "supplementary":
			sQualDesc = "1 000" # Total alcohol
	elif sQual == "E":
		sQualDesc = "eda" # net of drained weight
	elif sQual == "G":
		sQualDesc = " br" # Gross
	elif sQual == "M":
		sQualDesc = "mas" # net of dry matter
	elif sQual == "P":
		sQualDesc = "/ lactic matter" # of lactic matter
	elif sQual == "R":
		sQualDesc = "std qual" # of the standard quality
	elif sQual == "S":
		sQualDesc = "/ raw sugar"
	elif sQual == "T":
		sQualDesc = "/ dry lactic matter" # of dry lactic matter
	elif sQual == "X":
		sQualDesc = "hl" # Hectolitre
	elif sQual == "Z":
		sQualDesc = "% sacchar." # per 1% by weight of sucrose
	return sQualDesc

def fmtMarkdown(s):
	global sHeading2XML, sHeading3XML, sParaXML, sBulletXML
	s = re.sub("<table.*</table>", "", s, flags=re.DOTALL)
	s = re.sub("<sup>", "", s, flags=re.DOTALL)
	s = re.sub("</sup>", "", s, flags=re.DOTALL)
	s = re.sub("_", "\"", s, flags=re.DOTALL)
	sOut = ""
	a = s.split("\n")
	for ax in a:
		if ax[:2] == "##":
			sTemp = sHeading3XML
			sTemp = sTemp.replace("{HEADING}", ax.strip())
			sTemp = sTemp.replace("\.", ".")
			sTemp = sTemp.replace("##", "")
			sOut += sTemp
		elif ax[:4] == "  * ":
			sTemp = ax.strip()
			sTemp = sTemp.replace("* -", "")
			sTemp = sTemp.replace("* ", "")
			sTemp = sTemp.replace("\.", ".")
			sTemp = re.sub("^\([a-z]\) ", "", sTemp)
			sTemp = sBulletXML.replace("{TEXT}", sTemp)
			sOut += sTemp
		elif ax[:2] == "* ":
			sTemp = sParaXML
			sTemp = sTemp.replace("{TEXT}", ax.strip())
			sTemp = sTemp.replace("* ", "")
			sTemp = sTemp.replace("\.", ".")
			sOut += sTemp
		elif ax[:1] == "*":
			sTemp = sParaXML
			sTemp = sTemp.replace("{TEXT}", ax.strip())
			sTemp = sTemp.replace("*", "")
			sTemp = sTemp.replace("\.", ".")
			sOut += sTemp
		else:
			sTemp = sParaXML
			sTemp = sTemp.replace("{TEXT}", ax.strip())
			sTemp = sTemp.replace("* ", "")
			sTemp = sTemp.replace("\.", ".")
			if sTemp != "\n":
				sOut += sTemp
			
	return (sOut)
	
def zipdir(basedir, archivename):
	assert os.path.isdir(basedir)
	with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
		for root, dirs, files in os.walk(basedir):
			#NOTE: ignore empty directories
			for fn in files:
				absfn = os.path.join(root, fn)
				zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
				z.write(absfn, zfn)
