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

# Xử lý câu truy vấn AND
def process_query(arr,i):
	if i == 1:
		return 'SELECT DISTINCT duongdan,id_image FROM image as i,object as o,chitietdoituong as c WHERE i.id = c.id_image AND o.id = c.id_object AND o.name LIKE "%'+arr[i-1]+'%" ORDER BY o.probability DESC'
	elif i < len(arr):
		return 'SELECT DISTINCT tmp'+str(i)+'.duongdan,tmp'+str(i)+'.id_image FROM ('+process_query(arr,i-1)+') as tmp'+str(i)+',image as i,object as o,chitietdoituong as c WHERE i.id = c.id_image AND o.id = c.id_object AND c.id_image = tmp'+str(i)+'.id_image AND o.name LIKE "%'+arr[i-1]+'%" ORDER BY o.probability DESC'
	elif i == len(arr):
		return 'SELECT DISTINCT tmp'+str(i)+'.duongdan FROM ('+process_query(arr,i-1)+') as tmp'+str(i)+',image as i,object as o,chitietdoituong as c WHERE i.id = c.id_image AND o.id = c.id_object AND c.id_image = tmp'+str(i)+'.id_image AND o.name LIKE "%'+arr[i-1]+'%" ORDER BY o.probability DESC'


# Truy vấn lên cơ sở dữ liệu
def query_to_database():
	#chuyển danh từ số nhiều thành số ít
	singulars = convert_plural_to_singular()
	str1=' '.join(singulars)
	#chuyển các chữ số thành số
	arr = text2int(str1,numwords={})
	sql_and = process_query(arr,len(arr))
	print(sql_and)
	tmp = ''
	for i in arr:
		tmp += ' name LIKE '
		tmp += "\'%"+i+"%\'"
		if i != arr[-1]:
			tmp += ' OR'

	connection = cf.getConnection()
	try :
		cursor = connection.cursor()
		cursor.execute(sql_and)
		cursor1 = connection.cursor()
		sql_or = "SELECT i.duongdan FROM image as i,object as o,chitietdoituong as c WHERE i.id = c.id_image AND o.id = c.id_object AND ("+ tmp +") GROUP BY i.duongdan ORDER BY o.probability DESC"
		cursor1.execute(sql_or)
		new_arr = []
		for row in cursor:
			url = row['duongdan'].replace('-','/')
			if new_arr.count(url) == 0:
				new_arr.append(url)
		for row in cursor1:
			url1 = row['duongdan'].replace('-','/')
			if new_arr.count(url1) == 0:
				new_arr.append(url1)
		return new_arr
	except Exception as e:
		print(e)

@app.route('/result',methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		return render_template("searchpage.html", result = query_to_database(),content = get_data())

if __name__ == '__main__':
	app.run(debug = True)