class commodity(object):
	def __init__(self, goods_nomenclature_item_id):
		self.goods_nomenclature_item_id = goods_nomenclature_item_id
		self.chapter = goods_nomenclature_item_id[0:2]
        