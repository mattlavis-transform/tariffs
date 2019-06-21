import sys, os
from docxcompose.composer import Composer
from docx import Document

# Define the parameters - document type
try:
	sDocumentType = sys.argv[1]
except:
	sDocumentType = "schedule"

if sDocumentType == "s":
	sDocumentType = "schedule"
elif sDocumentType == "c":
	sDocumentType = "classification"

# Define the parameters - start document
try:
	iChapterStart = int(sys.argv[2])
except:
	iChapterStart = 1
	
# Define the parameters - end document
try:
	iChapterEnd   = int(sys.argv[3])
except:
	iChapterEnd   = iChapterStart
	
sChapter = str(iChapterStart).zfill(2)
print ("Adding TOC")

BASE_DIR		= os.path.dirname(os.path.abspath(__file__))
COMPONENT_DIR	= os.path.join(BASE_DIR, "xmlcomponents")
OUTPUT_DIR		= os.path.join(BASE_DIR, "output")
DEEP_DIR		= os.path.join(OUTPUT_DIR, sDocumentType)


file_master = os.path.join(COMPONENT_DIR, "toc_" + sDocumentType + ".docx")
master = Document(file_master)
composer = Composer(master)
for s in range(iChapterStart, iChapterEnd + 1):
	if s not in (77, 98, 99):
		sChapter = str(s).zfill(2)
		print ("Adding chapter " + sChapter)
		file_chapter = os.path.join(DEEP_DIR, sDocumentType + "_" + sChapter + ".docx")
		doc1 = Document(file_chapter)
		composer.append(doc1)

file_out = os.path.join(DEEP_DIR, sDocumentType + "_combined.docx")
composer.save(file_out)