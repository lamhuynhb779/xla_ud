import configdb as config
import json
import pymysql.cursors
# from chitietdoituong import *
# from myimage import *
# from myobject import *

# json_str = '{"images": [{"id": 1,"path": "test_images\image1.jpg","date": "2018-05-21","objects": [{"id": 1,"name": "dog","probability": 94,"id_image": 1,"soluong": 0},{"id": 2,"name": "dog","probability": 93,"id_image": 1,"soluong": 0}]},{"id": 2,"path": "test_images\image2.jpg","date": "2018-05-21","objects": [{"id": 2,"name": "person","probability": 91,"id_image": 2,"soluong": 0},{"id": 3,"name": "kite","probability": 82,"id_image": 2,"soluong": 0},{"id": 4,"name": "person","probability": 77,"id_image": 2,"soluong": 0},{"id": 5,"name": "kite","probability": 76,"id_image": 2,"soluong": 0},{"id": 6,"name": "kite","probability": 75,"id_image": 2,"soluong": 0},{"id": 7,"name": "person","probability": 63,"id_image": 2,"soluong": 0},{"id": 8,"name": "kite","probability": 60,"id_image": 2,"soluong": 0},{"id": 9,"name": "person","probability": 58,"id_image": 2,"soluong": 0},{"id": 10,"name": "person","probability": 51,"id_image": 2,"soluong": 0},{"id": 11,"name": "person","probability": 50,"id_image": 2,"soluong": 0}]},{"id": 3,"path": "test_images\image3.jpg","date": "2018-05-21","objects": [{"id": 3,"name": "person","probability": 88,"id_image": 3,"soluong": 0},{"id": 4,"name": "person","probability": 74,"id_image": 3,"soluong": 0},{"id": 5,"name": "person","probability": 74,"id_image": 3,"soluong": 0},{"id": 6,"name": "person","probability": 69,"id_image": 3,"soluong": 0},{"id": 7,"name": "person","probability": 65,"id_image": 3,"soluong": 0},{"id": 8,"name": "laptop","probability": 64,"id_image": 3,"soluong": 0},{"id": 9,"name": "laptop","probability": 55,"id_image": 3,"soluong": 0}]},{"id": 4,"path": "test_images\image4.jpg","date": "2018-05-21","objects": [{"id": 4,"name": "laptop","probability": 89,"id_image": 4,"soluong": 0},{"id": 5,"name": "laptop","probability": 81,"id_image": 4,"soluong": 0},{"id": 6,"name": "person","probability": 72,"id_image": 4,"soluong": 0},{"id": 7,"name": "laptop","probability": 50,"id_image": 4,"soluong": 0}]},{"id": 5,"path": "test_images\image5.jpg","date": "2018-05-21","objects": [{"id": 5,"name": "laptop","probability": 89,"id_image": 5,"soluong": 0},{"id": 6,"name": "person","probability": 66,"id_image": 5,"soluong": 0},{"id": 7,"name": "chair","probability": 60,"id_image": 5,"soluong": 0}]},{"id": 6,"path": "test_images\image6.jpg","date": "2018-05-21","objects": [{"id": 6,"name": "bottle","probability": 86,"id_image": 6,"soluong": 0},{"id": 7,"name": "bowl","probability": 70,"id_image": 6,"soluong": 0},{"id": 8,"name": "cake","probability": 53,"id_image": 6,"soluong": 0}]},{"id": 7,"path": "test_images\image7.jpg","date": "2018-05-21","objects": [{"id": 7,"name": "person","probability": 80,"id_image": 7,"soluong": 0},{"id": 8,"name": "person","probability": 73,"id_image": 7,"soluong": 0},{"id": 9,"name": "person","probability": 67,"id_image": 7,"soluong": 0},{"id": 10,"name": "person","probability": 62,"id_image": 7,"soluong": 0},{"id": 11,"name": "laptop","probability": 58,"id_image": 7,"soluong": 0},{"id": 12,"name": "person","probability": 57,"id_image": 7,"soluong": 0},{"id": 13,"name": "person","probability": 52,"id_image": 7,"soluong": 0}]},{"id": 8,"path": "test_images\image8.jpg","date": "2018-05-21","objects": [{"id": 8,"name": "person","probability": 97,"id_image": 8,"soluong": 0},{"id": 9,"name": "person","probability": 95,"id_image": 8,"soluong": 0},{"id": 10,"name": "person","probability": 92,"id_image": 8,"soluong": 0},{"id": 11,"name": "person","probability": 91,"id_image": 8,"soluong": 0},{"id": 12,"name": "person","probability": 89,"id_image": 8,"soluong": 0},{"id": 13,"name": "dining table","probability": 78,"id_image": 8,"soluong": 0},{"id": 14,"name": "bottle","probability": 53,"id_image": 8,"soluong": 0}]},{"id": 9,"path": "test_images\image9.jpg","date": "2018-05-21","objects": [{"id": 9,"name": "mouse","probability": 87,"id_image": 9,"soluong": 0},{"id": 10,"name": "bottle","probability": 80,"id_image": 9,"soluong": 0},{"id": 11,"name": "keyboard","probability": 60,"id_image": 9,"soluong": 0},{"id": 12,"name": "laptop","probability": 57,"id_image": 9,"soluong": 0}]}]}'

# def parseJSON(myjson):
# 	myjson = myjson.replace("\\", "-")
# 	# myjson = json.dumps(myjson)
# 	data = json.loads(myjson)
# 	images = data['images']
# 	for img in images:
# 		print(img['id'])

connection = config.getConnection()

def layIdLonNhat(table_name):
	global connection
	try:
		with connection.cursor() as cursor:
			sql = "SELECT id FROM "+table_name+" ORDER BY id DESC LIMIT 1"
			cursor.execute(sql)
			for row in cursor:
				return int(row['id'])
	except Exception as e:
		print(e)
	return 0

def themDuLieuBangImage(list_image):
	global connection
	for img in list_image:
		with connection.cursor() as cursor:
			try:
				sql = "INSERT INTO image (id, duongdan, ngaydang) VALUES (%s, %s, %s)"
				cursor.execute(sql, (img.getId(), img.getPath(), img.getDate()))
				connection.commit()
			except Exception as e:
				print(e)

def themDuLieuBangObject(list_object):
	global connection
	cursor = connection.cursor()
	for obj in list_object:
		try:
			sql = "INSERT INTO object (id, name, probability) VALUES (%s, %s, %s)"
			cursor.execute(sql, (obj.getId(), obj.getTenDoiTuong(), obj.getXacSuat()))
			connection.commit()
		except Exception as e:
			print(e)

def themDuLieuBangCTDT(list_ctdt):
	global connection
	cursor = connection.cursor()
	for ctdt in list_ctdt:
		try:
			sql = "INSERT INTO chitietdoituong (id_object, id_image) VALUES (%s, %s)"
			cursor.execute(sql, (ctdt.getIdObject(), ctdt.getIdImage()))
			connection.commit()
		except Exception as e:
			print(e)