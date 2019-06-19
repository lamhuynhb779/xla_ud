import glob, shutil, os

source = 'E:\\xulyanhvaungdung\\xla_ud\\models-master\\object_detection\\'
dest = 'E:\\xulyanhvaungdung\\xla_ud\\models-master\\object_detection\\xulytruyvan\\lay_du_lieu_tu_flile_html\\static\\test_images\\'

def moveFile(file):
	global source
	global dest
	shutil.move(source + file, dest)

def countFile():
	path = 'E:\\xulyanhvaungdung\\xla_ud\\models-master\\object_detection\\test_images\\'
	typefile = ['*.jpg', '*.png']
	count = 0
	for tf in typefile:
		files = glob.glob(path+tf)
		count += len(files)
	return count

def getAllImage():
	fs = os.listdir('E:\\xulyanhvaungdung\\xla_ud\\models-master\\object_detection\\test_images\\')
	files_img = ["test_images/"+i for i in fs if i.endswith('.jpg')]
	return files_img