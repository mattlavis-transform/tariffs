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

if __name__ == '__main__':
	import sys
	basedir = sys.argv[1]
	archivename = sys.argv[2]
	zipdir(basedir, archivename)
	
	
# py zip3.py "C:\\projects\\create_tariff_schedule\\Python2\\test2\\" "test.docx" 