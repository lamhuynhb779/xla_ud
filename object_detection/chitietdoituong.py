class ChiTietDoiTuong:
	def __init__(self):
		self.id_object = 0
		self.id_image = 0
		print('Khoi tao doi tuong ctdt')

	def getIdObject(self):
		return self.id_object

	def setIdObject(self, myid):
		self.id_object = myid

	def getIdImage(self):
		return self.id_image

	def setIdImage(self, myid):
		self.id_image = myid

	def toString(self):
		print("id_obj: %s,id_img: %s,sl: %s" %(self.id_object, self.id_image))