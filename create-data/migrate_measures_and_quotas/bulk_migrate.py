import classes.globals as g
import os
import sys
import csv

"""
Examples of how to call


"""

app = g.app
app.override_prompt = True

print (app.bulk_migration_profile)
print (app.bulk_migrations_list[app.bulk_migration_profile])
#sys.exit()
migrations_file = os.path.join(app.SOURCE_DIR,	app.bulk_migrations_list[app.bulk_migration_profile])

with open(migrations_file) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter = ",")
	for row in csv_reader:
		if len(row) > 0:
			regulation_from = row[0]
			try:
				regulation_to = row[1]
			except:
				regulation_to = ""

			print (regulation_from, regulation_to)

			if len(regulation_from) == 7:
				if regulation_to != "":
					os.system("python3 migrate_measures.py r r " + regulation_from + " " + regulation_to)
				else:
					os.system("python3 migrate_measures.py r t " + regulation_from)

sys.exit()
