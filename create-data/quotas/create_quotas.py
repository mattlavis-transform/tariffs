import classes.globals as g
import os
import sys

g.app.get_measures_from_csv()
g.app.get_all_origins_from_db()
g.app.get_quota_definitions_from_csv()
g.app.get_quota_order_numbers_from_csv()
g.app.compare_order_number_origins()

g.app.write_xml()
g.app.set_config()
g.app.validate()
