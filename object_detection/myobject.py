class MyObject:
	def __init__(self):
		self.id = 0
		self.name = ""
		self.prob = 0
		print('Khoi tao doi tuong object')

	def getId(self):
		return self.id

	def setId(self, myid):
		self.id = myid

	def getTenDoiTuong(self):
		return self.name

	def setTenDoiTuong(self, name):
		self.name = name

	def	getXacSuat(self):
		return self.prob

	def setXacSuat(self, prob):
		self.prob = prob

	def toString(self):
		print("id: %s, tendoituong: %s, xacsuat: %s" %(self.id, self.name, self.prob))