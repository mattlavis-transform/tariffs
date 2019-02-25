import re
import sys
from datetime import datetime

from classes.commodity import commodity
import classes.functions as fn
import classes.globals as g

class chapter(object):
	def __init__(self, chapter_id_number):
		# Get parameters from instantiator
		self.commodity_list		= []
		self.chapter_id_number	= chapter_id_number
		self.chapter_id_string	= str(chapter_id_number).zfill(2)
		print (" - Getting chapter", self.chapter_id_string)
		self.set_zeroes()
		self.mfn_component_list = []
		self.insert_mfns()

		self.create_xml()

	def insert_mfns(self):
		# Find all the specific MFNs that belong to this chapter
		for obj in g.app.mfn_master_list:
			chap = obj.goods_nomenclature_item_id[0:2]
			if chap == self.chapter_id_string:
				if obj.duty_amount >= 0:
					self.mfn_component_list.append(obj)
				#print ("Appending")

		# Now loop through all of the relevant commodity codes that are non-zero
		# and find the children
		for obj in self.mfn_component_list:
			if obj.duty_amount != 0:
				for my_commodity in self.commodity_list:
					if (my_commodity.goods_nomenclature_item_id == obj.goods_nomenclature_item_id) and (my_commodity.productline_suffix == "80"):
						#if my_commodity.goods_nomenclature_item_id == "0204230000":
						#	print ("Match")
						leaf = my_commodity.leaf
						if leaf == "1":
							# If the found MFN is already a leaf, then all that needs to happen is for the MFN
							# to replace the existing component on the same leaf node
							my_commodity.drop_zero_component()
							my_commodity.append_component(obj.duty_expression_id, obj.duty_amount, obj.monetary_unit_code, obj.measurement_unit_code, obj.measurement_unit_qualifier_code)
						else:
							# However, if the found MFN is not on a leaf, then we need to assign it to leaves
							# instead of the level to which is is assigned in the spreadsheet
							# print ("is not leaf", my_commodity.goods_nomenclature_item_id, obj.duty_amount)
							my_commodity.get_hierarchy(self.commodity_list)

							if my_commodity.goods_nomenclature_item_id == "0204230000":
								print (len(my_commodity.leaf_children))
							for child in my_commodity.leaf_children:
								#if my_commodity.goods_nomenclature_item_id == "0204230000":
								#	print ("Here", my_commodity.goods_nomenclature_item_id, child.goods_nomenclature_item_id)
								child.drop_zero_component()
								child.append_component(obj.duty_expression_id, obj.duty_amount, obj.monetary_unit_code, obj.measurement_unit_code, obj.measurement_unit_qualifier_code)


	def create_xml(self):
		self.xml = ""
		for my_commodity in self.commodity_list:
			if my_commodity.leaf == "1":
				self.xml += my_commodity.xml()


	def set_zeroes(self):
		sql = """SELECT goods_nomenclature_sid, goods_nomenclature_item_id, producline_suffix, 
		number_indents, leaf, description FROM  ml.goods_nomenclature_export_brexit('""" + self.chapter_id_string + """%') ORDER BY 2, 3"""
		#print (sql)
		cur = g.app.conn.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		for row in rows:
			goods_nomenclature_sid		= row[0]
			goods_nomenclature_item_id	= row[1]
			productline_suffix         	= row[2]
			number_indents            	= row[3]
			leaf			           	= row[4]
			description		           	= row[5]
			my_commodity = commodity(goods_nomenclature_sid, goods_nomenclature_item_id, productline_suffix, number_indents, leaf, description)
			self.commodity_list.append (my_commodity)

	def deal_with_double_zeroes(self):
		if (self.number_indents == 0):
			if (self.goods_nomenclature_item_id[-8:] == "00000000"):
				self.number_indents = -1
