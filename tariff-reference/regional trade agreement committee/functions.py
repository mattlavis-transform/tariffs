# Import standard modules
from __future__ import with_statement
import psycopg2
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime
import os
import sys
import codecs
import re

# Import custom modules
from application import application
from workbook import workbook

app = application()
wkbk = workbook()
#print ("Instantiated workbook")

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

def fmtMeasureTypeDescription(s):
	s = s.replace("end-use", "authorised use")
	return s
	
def fmtDate(d):
	try:
		d = datetime.strftime(d, '%d-%m-%y')
	except:
		d = ""
	return d
	
def fmtMarkdown(s):
	s = re.sub("<table.*</table>", "", s, flags=re.DOTALL)
	s = re.sub("<sup>", "", s, flags=re.DOTALL)
	s = re.sub("</sup>", "", s, flags=re.DOTALL)
	s = re.sub("_", "\"", s, flags=re.DOTALL)
	s = s.replace("  ", " ")
	sOut = ""
	a = s.split("\n")
	for ax in a:
		if ax[:2] == "##":
			sTemp = app.sHeading3XML
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
			sTemp = app.sBulletXML.replace("{TEXT}", sTemp)
			sOut += sTemp
		elif ax[:2] == "* ":
			sTemp = app.sParaXML
			sTemp = sTemp.replace("{TEXT}", ax.strip())
			sTemp = sTemp.replace("* ", "")
			sTemp = sTemp.replace("\.", ".")
			sOut += sTemp
		elif ax[:1] == "*":
			sTemp = app.sParaXML
			sTemp = sTemp.replace("{TEXT}", ax.strip())
			sTemp = sTemp.replace("*", "")
			sTemp = sTemp.replace("\.", ".")
			sOut += sTemp
		else:
			sTemp = app.sParaXML
			sTemp = sTemp.replace("{TEXT}", ax.strip())
			sTemp = sTemp.replace("* ", "")
			sTemp = sTemp.replace("\.", ".")
			if sTemp != "\n":
				sOut += sTemp
			
	return (sOut)
	
def zipdir(archivename):
	BASE_DIR     = os.path.dirname(os.path.realpath(__file__))
	MODEL_DIR = os.path.join(BASE_DIR, "model")
	with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
		for root, dirs, files in os.walk(MODEL_DIR):
			#NOTE: ignore empty directories
			for fn in files:
				absfn = os.path.join(root, fn)
				zfn = absfn[len(MODEL_DIR)+len(os.sep):] #XXX: relative path
				z.write(absfn, zfn)

def mstr(x):
	if x is None:
		return ""
	else:
		return str(x)

def mnum(x):
	if x is None:
		return ""
	else:
		return int(x)

def debug(x):
	if app.debug:
		print (x)

def surround(x):
	if "<w:t>" in x:
		return x
	else:
		return "<w:r><w:t>" + x + "</w:t></w:r>"

def fmtSeasonal(s):
	s = mstr(s)
	s = s.replace("EUR", "€")
	s = s.replace("DTN G", "/ 100 kg gross")
	s = s.replace("DTN", "/ 100 kg")
	return s

