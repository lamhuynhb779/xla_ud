class MyImage:
	def __init__(self):
		self.id = 0
		self.path = ""
		self.date = ""
		print('Khoi tao doi tuong image')

	def getId(self):
		return self.id

	def setId(self, myid):
		self.id = myid

	def getPath(self):
		return self.path

	def setPath(self, path):
		path = path.replace("\\","-")
		self.path = path

	def	getDate(self):
		return self.date

	def setDate(self, mydate):
		self.date = mydate

	def toString(self):
		print("id: %s, path: %s, date: %s" %(self.id, self.path, self.date))