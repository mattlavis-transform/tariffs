# Imported modules
import csv
import os
import codecs
from csv import QUOTE_ALL

# custom modules
import functions as f
from functions import app
from functions import mstr
from functions import mnum
from functions import fmtDate

# class modules
from application import application
from footnote import footnote

#################################################################
# Loop through all of the footnotes
#################################################################
app = f.app
app.getFoonotes()
app.resolveFootnotes()
print (app.cnt)
app.writeResults()
