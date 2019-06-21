from __future__ import with_statement
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
import os


def zipdir(basedir, archivename):
	assert os.path.isdir(basedir)
	with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
		for root, dirs, files in os.walk(basedir):
			#NOTE: ignore empty directories
			for fn in files:
				absfn = os.path.join(root, fn)
				zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
				z.write(absfn, zfn)



path = "C:\\projects\\create_tariff_schedule\\xmlcomponents\\"

fDocument = open(path + "document.xml", "r") 
sDocument = fDocument.read()

fTitle = open(path + "document.xml", "r") 
sTitle = fTitle.read()

fDocument = open(path + "document.xml", "r") 
sDocument = fDocument.read()

fDocument = open(path + "document.xml", "r") 
sDocument = fDocument.read()

fTable = open(path + "table.xml", "r") 
sTable = fTable.read()

sDocument = sDocument.replace("{BODY}", sTable)

print (sDocument)

file = open("C:\\projects\\create_tariff_schedule\\test\\model\\word\\document.xml", "w") 
file.write(sDocument) 
file.close() 


basedir = "C:\\projects\\create_tariff_schedule\\test\\model"
archivename = "model.docx"
zipdir(basedir, archivename)
