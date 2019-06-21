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

app = functions.app
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

app.shutDown()
