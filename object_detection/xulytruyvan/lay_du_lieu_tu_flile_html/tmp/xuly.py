from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from flask import Flask, render_template, request
from textblob import TextBlob
import config as cf

app = Flask(__name__)

# Lấy dữ liệu từ thanh tim kiếm
def get_data():
	response = request.form['text']
	return response

# Loại bỏ những stopword
def remove_stopword():
	content = get_data()
	stop_words = set(stopwords.words('english'))
	word_tokens = word_tokenize(content)
	filtered_sentence = []

	for w in word_tokens:
		if w not in stop_words:
			filtered_sentence.append(w)
	return filtered_sentence

# Chuyển chữ số thành số
def text2int(textnum, numwords={}):
	arr = []
	if not numwords:
		units = [
			"zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
			"nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
			"sixteen", "seventeen", "eighteen", "nineteen",
		]

		tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

		scales = ["hundred", "thousand", "million", "billion", "trillion"]

		numwords["and"] = (1, 0)
		for idx, word in enumerate(units):	numwords[word] = (1, idx)
		for idx, word in enumerate(tens):	numwords[word] = (1, idx * 10)
		for idx, word in enumerate(scales):	numwords[word] = (10 ** (idx * 3 or 2), 0)

	current = result = 0
	for word in textnum.split():
		if word not in numwords:
			arr.append(word)
		else:
			scale, increment = numwords[word]
			current = current * scale + increment
			if scale > 100:
				result += current
				current = 0
			arr.append(str(result + current))
	return arr

# Chuyển danh từ số nhiều thành số ít
def convert_plural_to_singular():
	# Chuyển mảng đã xóa stopword thành chuỗi 
	words=' '.join(remove_stopword())
	blob = TextBlob(words)
	singulars = [word.singularize() for word in blob.words]
	return singulars

# Truy vấn lên cơ sở dữ liệu
def query_to_database():
	#chuyển danh từ số nhiều thành số ít
	singulars = convert_plural_to_singular()
	str1=' '.join(singulars)
	#chuyển các chữ số thành số
	arr = text2int(str1,numwords={})

	connection = cf.getConnection()
	new_arr = []

	# x = "select id from (select id from image) AS KQ, chitietdoituong AS c WHERE KQ.id = c.id_image"
	# # x = "select id from image INTO KQ"
	# cursor = connection.cursor()
	# cursor.execute(x)
	# # cursor.execute("SELECT * FROM KQ")
	# for row in cursor:
	# 	print(row['id'])
		
	#Truy vấn AND
	# t = 0; elements = len(arr); tmp = ''
	# for i in range(elements):
	# 	if i != elements-1:
	# 		# tmp += "SELECT i.id FROM image as i, object as o, chitietdoituong as c WHERE i.id = c.id_image AND c.id_object = o.id AND o.name LIKE \'%"+arr[i]+"%\' INTO KQ"+ str(t)+"; "
	# 		tmp += "CREATE TEMPORARY TABLE KQ"+ str(t) +" SELECT i.id FROM image as i, object as o, chitietdoituong as c WHERE i.id = c.id_image AND c.id_object = o.id AND o.name LIKE \'%"+arr[i]+"%\'; "
	# 	else:
	# 		bang_dong = ''
	# 		ket_bang = ''
	# 		for j in range(t):
	# 			if j != t - 1:
	# 				bang_dong += 'KQ'+str(j)+', '
	# 				if j != 0:
	# 					ket_bang += "KQ"+str(j-1)+".id = "
	# 				ket_bang += "KQ"+str(j)+".id "
	# 				ket_bang += "AND "
	# 			else:
	# 				bang_dong += 'KQ'+str(j)
	# 				ket_bang += "KQ"+str(j-1)+".id = "
	# 				ket_bang += "KQ"+str(j)+".id"
	# 		if elements == 1:
	# 			tmp += " SELECT DISTINCT i.duongdan FROM image as i, object as o, chitietdoituong as c WHERE i.id = c.id_image AND c.id_object = o.id AND o.name LIKE \'%"+arr[i]+"%\'"
	# 		else:
	# 			tmp += " SELECT DISTINCT i.duongdan FROM image as i, object as o, chitietdoituong as c, "+ bang_dong +" WHERE i.id = c.id_image AND c.id_object = o.id AND i.id = "+ ket_bang +" AND o.name LIKE \'%"+arr[i]+"%\'"
	# 	t += 1
	# print(tmp)
	# try :
	# 	cursor = connection.cursor()
	# 	sql = tmp
	# 	cursor.execute(sql)

	# 	for row in cursor:
	# 		url = row['duongdan'].replace('-','/')
	# 		new_arr.append(url)
	# except Exception as e:
	# 	print(e)
	# print(new_arr)

	# ---------------------------------------------
	t = 0; elements = len(arr); tmp = ''
	for i in range(elements):
		if i != elements-1:
			tmp += "(SELECT i.id FROM image as i, object as o, chitietdoituong as c WHERE i.id = c.id_image AND c.id_object = o.id AND o.name LIKE \'%"+arr[i]+"%\') AS KQ"+str(t)
			if i != elements-2: 
				tmp += ", "
		else:
			ket_bang = ''
			for j in range(t):
				if j != t - 1:
					if j != 0:
						ket_bang += "KQ"+str(j-1)+".id = "
					ket_bang += "KQ"+str(j)+".id "
					ket_bang += "AND "
				else:
					ket_bang += "KQ"+str(j-1)+".id = "
					ket_bang += "KQ"+str(j)+".id"
			if elements == 1:
				tmp = " SELECT DISTINCT i.duongdan FROM image as i, object as o, chitietdoituong as c WHERE i.id = c.id_image AND c.id_object = o.id AND o.name LIKE \'%"+arr[i]+"%\'"
			else:
				tmp = " SELECT DISTINCT i.duongdan FROM image as i, object as o, chitietdoituong as c, "+ tmp +" WHERE i.id = c.id_image AND c.id_object = o.id AND i.id = "+ ket_bang +" AND o.name LIKE \'%"+arr[i]+"%\'"
		t += 1
	print(tmp)
	try :
		cursor = connection.cursor()
		sql = tmp
		cursor.execute(sql)

		for row in cursor:
			url = row['duongdan'].replace('-','/')
			new_arr.append(url)
	except Exception as e:
		print(e)
	print(new_arr)

	#Truy vấn OR
	tmp = ''
	for i in arr:
		tmp += ' name LIKE '
		tmp += "\'%"+i+"%\'"
		if i != arr[-1]:
			tmp += ' OR'
	try :
		cursor = connection.cursor()
		sql = "SELECT i.duongdan FROM image as i,object as o,chitietdoituong as c WHERE i.id = c.id_image AND o.id = c.id_object AND ("+ tmp +") GROUP BY i.duongdan ORDER BY o.probability DESC"
		cursor.execute(sql)
		new_arr = []
		for row in cursor:
			url = row['duongdan'].replace('-','/')
			new_arr.append(url)
		return new_arr
	except Exception as e:
		print(e)

@app.route('/result',methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		return render_template("searchpage.html", result = query_to_database(),content = get_data())

if __name__ == '__main__':
	app.run(debug = True)