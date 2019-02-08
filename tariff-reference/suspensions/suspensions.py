# Import standard modules
import sys
import glob as g
import functions as f
from commodity import commodity

# Set up
app = g.app
app.get_DavidOwen_list()
app.getSectionsChapters()
app.get_suspensions()
app.write_file()
app.shutDown()
print ("\nPROCESS COMPLETE\n")