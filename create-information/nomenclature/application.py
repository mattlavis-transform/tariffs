import psycopg2
import os
import csv
import sys
import codecs
import re

from commodity import commodity	

class application(object):
	def __init__(self):
		self.conn = psycopg2.connect("dbname=trade_tariff_181212b user=postgres password=zanzibar")
		self.BASE_DIR	= os.path.dirname(os.path.abspath(__file__))
		self.CSV_DIR	= os.path.join(self.BASE_DIR, "csv")
		self.MFN_DIR	= os.path.join(self.BASE_DIR, "mfn")
		self.commodity_list = []

	def create_csv(self):
		filename = os.path.join(self.CSV_DIR, "all.csv")
		with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
			filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			filewriter.writerow(["Commodity", "Suffix", "Start", "End", "Description", "Indents"])
			for i in range(0, 10):
				s = str(i)
				print (s)
				sql = """SELECT goods_nomenclature_item_id, producline_suffix, description,
				number_indents, leaf FROM ml.goods_nomenclature_export_2019 ('""" + s + """%') ORDER BY 1, 2"""
				cur = self.conn.cursor()
				cur.execute(sql)
				rows = cur.fetchall()
				for m in rows:
					goods_nomenclature_item_id	= m[0]
					productline_suffix			= m[1]
					description					= m[2]
					number_indents				= m[3]
					leaf						= m[4]
					if productline_suffix == "80":
						filewriter.writerow([goods_nomenclature_item_id, productline_suffix, number_indents, leaf, description])

	def analyse_mfns(self):
		# Get the whole commodity code tree
		filename = os.path.join(self.CSV_DIR, "all.csv")
		with open(filename, "r", encoding='utf-8') as f:
			reader = csv.reader(f)
			list_all = list(reader)
		
		list_all2 = []
		list_count = len(list_all)
		print (list_count)
		for rw in list_all:
			list_all2.append(rw[0])
		
		# Get the MFNs only
		filename = os.path.join(self.MFN_DIR, "liberalisation_exemptions.csv")
		with open(filename, "r") as f:
			reader = csv.reader(f)
			list_exemptions_master = list(reader)
		f.close()
		list_exemptions_master.sort()

		# Rewrite the file, sorted
		filename2 = os.path.join(self.MFN_DIR, "liberalisation_exemptions_sorted.csv")
		list_exemptions_master2 = []
		with open(filename2, "w") as f:
			for item in list_exemptions_master:
				list_exemptions_master2.append (item[0] + "00")
				f.write(item[0] + "\n")
		f.close()

		# Loop through the exceptions and locate any child leaf items
		leaf_count = 0
		filename	= os.path.join(self.MFN_DIR, "mfn_exceptions_exploded.csv")
		f = open(filename, "w")
		#print (list_exemptions_master)
		#sys.exit()
		list_out = []
		for row in list_exemptions_master:
			liberalised_item	= row[0] + "00"
			start_index			= 0
			try:
				start_index	= list_all2.index(liberalised_item)
				my_indents	= list_all[start_index][2]
				leaf		= list_all[start_index][3]
				if leaf == "1":
					print ("Found master leaf")
					leaf_count += 1
					f.write(liberalised_item + "\n")
					list_out.append(liberalised_item)
					print(liberalised_item)

			except:
				start_index = 0

			if start_index != 0:
				for i in range(start_index + 1, list_count):
					if list_all[i][2] > my_indents:
						if list_all[i][0] not in (list_exemptions_master2) and list_all[i][0] not in list_out:
							if list_all[i][0] > liberalised_item and list_all[i][3] == "1":
								leaf_count += 1
								list_out.append(list_all[i][0])
								#f.write(liberalised_item + "," + list_all[i][0] + "\n")
								f.write(list_all[i][0] + "\n")
						else:
							pass
					elif list_all[i][2] <= my_indents:
						break

		print (leaf_count)
