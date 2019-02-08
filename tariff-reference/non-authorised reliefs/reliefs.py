# Import standard modules
import sys
import glob as g
import functions as f
from commodity import commodity

# Set up
app = g.app
app.get_mfn_rates()
app.get_special_paragraphs()
app.get_DavidOwen_list()
app.getSectionsChapters()
app.get_reliefs()
app.write_file()
app.shutDown()
print ("\nPROCESS COMPLETE\n")