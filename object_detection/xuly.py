import myimage as mi
import myobject as mo
import chitietdoituong as ctdt
import datetime, time
import re
from collections import Counter

pattern_name = '[a-zA-Z]+ [a-zA-Z]+|[a-zA-Z]+'
pattern_prob = '\d+'

def thietLapListImage(image_path, id_image, list_img):
	mydate = datetime.datetime.now().strftime("%Y-%m-%d")
	my_img = mi.MyImage()
	my_img.setId(id_image)
	my_img.setPath(image_path)
	my_img.setDate(mydate)
	list_img.append(my_img)

def thietLapListObjectVaChiTietDoiTuong(display_str_list, id_image, id_object, list_obj, list_ctdt):
	list_name_object = []
	for display_str in display_str_list:
		my_name_obj = re.findall(pattern_name, display_str)
		my_prob_obj = re.findall(pattern_prob, display_str)

		my_obj = mo.MyObject()
		my_obj.setId(id_object[0])
		my_obj.setTenDoiTuong(my_name_obj[0])
		my_obj.setXacSuat(my_prob_obj[0])

		my_ctdt = ctdt.ChiTietDoiTuong()
		my_ctdt.setIdObject(id_object[0])
		my_ctdt.setIdImage(id_image[0])

		list_name_object.append(my_name_obj[0])

		list_obj.append(my_obj)
		list_ctdt.append(my_ctdt)

		id_object[0] += 1
	Counter(list_name_object)