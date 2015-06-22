from bs4 import BeautifulSoup
import re
import urllib2
import MySQLdb

db = MySQLdb.connect("localhost","root","8520","Docinfo")
cursor = db.cursor()

soup = BeautifulSoup(open("sulekha2.html"))

# print soup.prettify()
lis = {"Phone/Mobile":"Not found","description":"Not found","pull-left":"Not found","Address":"Not found","Email":"Not found","Website":"Not found","Contact Person":"Not found","Working Hours":"Not found","Categories":"Not found"}
divname = soup.find_all("div",{"class":"pull-left"})
divdesc = soup.find_all("div",{"itemprop":"description"})
print divname[0].text
# print divname[0]['class'][0]
# print divdesc[0]['class'][0]
lis.update({"pull-left" : divname[0].text.replace("'","\\'").encode('utf8') })
lis.update({"description" : divdesc[0].text.replace("'","\\'").encode('utf8')})
# lis.update({"pull-left" : divdesc[0].contents[1].p.contents[0] })
# lis.update({"description" : divname[0].h1.string})

# if divdesc[0].p['id'] == "showmore":
# 	print "y"
# 	print divdesc[0].contents[1].p.contents[0]
# print divdesc[0].contents[1].p.contents


# print divname[0].h1.string
div2= soup.find_all("div",{"class":"profile-list"})
for item in div2:
	li2 = item.find_all("li",{"class":"row"})
	# lis={}
	

	for item2 in li2:
	 	dv1= item2.find_all("div",{"class":"profile-details"})
	 	dv2=item2.find_all("div",{"class":"profile-child"})
	 	

	 	
	 	for a in dv1:
	 		# print a.strong.text,":::", " ".join(a.div.text.split())#a.div.text.strip('\n\r')
	 		# lis.append(a.div.text)
	 		lis.update({a.strong.text.replace("'","\\'").encode('utf8') : " ".join(a.div.text.split()).replace("'","\\'").encode('utf8') })
	print "@@@@@########$$$$"
	print lis
	# lis.append("null")
	# print lis
	# sql = "INSERT INTO `Doc Info`(`Phone`, `Address`, `Email`, `Website`, `Contact Person`, `Working hrs`, `Categories`,`About`, `Clinic name`) VALUES (" +"'" +lis["Phone/Mobile"]+"'"+",'"+lis["Address"]+"'"+",'"+lis["Email"]+"'"+",'"+lis["Website"]+"'"+",'"+lis["Contact Person"]+"'"+",'"+lis["Working Hours"]+"'"+",'"+lis["Categories"]+"'"+",'"+lis["description"]+"'"+",'"+lis["pull-left"]+"'"+")"

	sql = "INSERT INTO `Doc Info`( `Phone/Mobile`, `Address`, `Email`, `Website`, `Contact Person`, `Working hours`, `Categories`, `About`, `Clinic name`)VALUES (" +"'" +lis["Phone/Mobile"]+"'"+",'"+lis["Address"]+"'"+",'"+lis["Email"]+"'"+",'"+lis["Website"]+"'"+",'"+lis["Contact Person"]+"'"+",'"+lis["Working Hours"]+"'"+",'"+lis["Categories"]+"'"+",'"+lis["description"]+"'"+",'"+lis["pull-left"]+"'"+")"

	# sql = "INSERT INTO `test`(`Phone`, `Address`, `Email`, `Website`, `Contact Person`, `Working hrs`, `Categories`) VALUES (" +"'" +lis[0]+"'"+",'"+lis[1]+"'"+",'"+lis[2]+"'"+",'"+lis[3]+"'"+",'"+lis[4]+"'"+",'"+lis[5]+"'"+",'"+lis[6]+"'"+")"
	print sql
	cursor.execute(sql)
	db.commit()

 		# sql = "INSERT INTO test('1','kumar','19','m','000','fada','asdad')"
 		# cursor.execute(sql)
 		# db.commit
	 	# print dv2[0].string,"@@@@@@@@@@"
	 	# for a in dv2:
	 	# 	print a.text
	 	# print type(dv1)
	 	# f.write(str( dv1[0].contents[0].contents[0])+'\n')
	 	# print dv2[0].contents[0]