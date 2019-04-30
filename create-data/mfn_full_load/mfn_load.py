import classes.globals as g
import os
import sys

g.app.get_measures_components_from_csv()
g.app.get_measures_from_csv()

#g.app.get_nomenclature_dates()

g.app.write_xml()
g.app.validate()
g.app.set_config()