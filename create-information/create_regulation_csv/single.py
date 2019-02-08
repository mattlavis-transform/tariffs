import psycopg2
import os
import sys
import functions

from application import application

app = functions.app
regulation_id = sys.argv[1]
print ("Creating document for regulation " + regulation_id)
app.createRegulationCSV(regulation_id)