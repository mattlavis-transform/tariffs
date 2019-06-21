# Import standard modules
from __future__ import with_statement
import psycopg2
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
import os
import sys
import codecs
import re
import functions

# Import custom modules
from application import application
from chapter     import chapter
#from workbook	 import workbook

app = functions.app
wkbk = functions.wkbk
wkbk.create_workbook(app)
wkbk.write_headers()

app.getSectionsChapters()
app.readTemplates()

if app.sDocumentType == "schedule":
	app.getSivs()
	app.getITAProducts()
	app.getAuthorisedUse()
	app.getSeasonal()
	app.getSpecials()

for i in range(app.iChapterStart, app.iChapterEnd + 1):
	oChapter = chapter(i)
	oChapter.formatChapter()
wkbk.close_workbook()

app.shutDown()
