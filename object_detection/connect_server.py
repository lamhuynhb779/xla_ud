import urllib.request
import urllib
mydata=[('one','1'),('two','2')]#The first is the var name the second is the value
mydata=urllib.urlencode(mydata)
path='http://localhost:8080/DoAnTruyVan_DetectObject/demo.php'#the url you want to POST to
req=urllib.request.Request(path, mydata)
req.add_header("Content-type", "application/x-www-form-urlencoded")
page=urllib.request.urlopen(req).read()
print(page)