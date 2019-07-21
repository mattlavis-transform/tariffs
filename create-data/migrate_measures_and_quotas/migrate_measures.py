import classes.globals as g
import os
import sys

#from application import application 
"""
Examples of how to call
py migrate_measures.py m r supp N1010101 ZA - Migrate supplementary units that relate to S. Africa
py migrate_measures.py r t D1700370 N1010101 ZA - Migrate all measures from a regulation to another that are related to S. Africa

"""

app = g.app
app.get_templates()
app.get_envelope()

app.get_mfns()
app.get_measures()
app.get_measure_conditions()
app.get_measure_condition_components()
app.get_measure_components()
app.get_measure_geographical_exclusions()
app.get_measure_footnotes()
app.get_measure_partial_temporary_stops()

app.terminate_measures()
app.restart_measures()

app.write_content()
app.validate(app.output_filename)
#app.generate_xml_report()
#app.check_business_rules()
app.copy_to_custom_import_folder()
app.set_config()