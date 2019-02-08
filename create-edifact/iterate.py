import os
import sys
import functions

folders = []
files = []

folder = "C:\\projects\\taric_edifact_convert\\xml\\"
for entry in os.scandir(folder):
	if entry.is_dir():
		folders.append(entry.path)
	elif entry.is_file():
		filename = entry.path.replace(folder, "")
		functions.doConvert(filename)
