import sys
from docxcompose.composer import Composer
from docx import Document

# Define the parameters - document type
try:
	sDocumentType = sys.argv[1]
except:
	sDocumentType = "schedule"

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
master = Document("xmlcomponents\\toc_" + sDocumentType + ".docx")
composer = Composer(master)
for s in range(iChapterStart, iChapterEnd + 1):
	if s not in (77, 98, 99):
		sChapter = str(s).zfill(2)
		print ("Adding chapter " + sChapter)
		doc1 = Document("output\\" + sDocumentType + "\\" + sDocumentType + "_" + sChapter + ".docx")
		composer.append(doc1)

composer.save("output\\" + sDocumentType + "\\" + sDocumentType + "_combined.docx")