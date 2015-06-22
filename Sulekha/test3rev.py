from bs4 import BeautifulSoup
import re
import urllib2
import MySQLdb

db = MySQLdb.connect("localhost","root","8520","Docinfo")
cursor = db.cursor()

lisdic = {"ratingtot": "not found","review": "not found","usrrate": "not found","name": "not found","docname": "not found","link": "not found","badge": "not found"}

#file is used to extract badge, reviews,and ratings test
soup2 = BeautifulSoup(open("sulekha4.html"))
# print soup2.prettify().encode('utf-8')
# print soup2.prettify()

ratingtot= soup2.find_all("div" , {"class":"span6"})
# print ratingtot[0].text
try:
	lisdic.update({"ratingtot":ratingtot[0].text})
	# print lisdic["ratingtot"]
except:
	pass

#####getting review
reviewlis = soup2.find_all("li" , {"class":"review-item"})
# print reviewlis
lisusrlis=[]
if reviewlis:
	
	try:
		for a in reviewlis:
			usrlis=[]
			revpar = a.find_all("div",{"class":"top-review-right"})
			# print revpar[0].p.text				#review
			# print revpar[0].div.span.text		#rating
			# print revpar[0].h3.text#+'@@@@@@'+'\n'  #name
			# print "@@@@@@@@@"+'\n'
			usrlis.append(revpar[0].p.text.encode('utf-8'))
			usrlis.append(revpar[0].div.span.text.encode('utf-8'))
			usrlis.append(revpar[0].h3.text.encode('utf-8'))
			lisusrlis.append(usrlis)
			# print usrlis
			# print "@@@@@@"+'\n'
		# print lisusrlis
		# print "$$$$$$$"
	except:
		lisusrlis.append("SORRY!! ")
		print lisusrlis
else:
	lisusrlis.append("SORRY!! no reviews were found ")
	print lisusrlis




badge = soup2.find_all("div",{"class":"manage-prolink"})
# print badge[0].span['class'][1]
try:
	lisdic.update({"badge":badge[0].span['class'][1]})
	print lisdic["badge"]
except:
	lisdic.update({"badge":"Sorry !! badge not found"})


######to find featured in of doc
lisfeatr = []
featured=soup2.find_all("span",{"class":"featured"})
# print featured#.encode('utf-8')
if featured:
	atag= featured[0].find_all("a")
	# print atag
	try:
		for a in atag:
			if(a['href']=="#prdservice"):
				featuredsm = soup2.find_all("ul",{"class":"expert-list"})
				# print featuredsm
				for a in featuredsm:
					for li_item in a.find_all("li"):
						# print li_item.text
						lisfeatr.append(li_item.text.encode('utf-8'))
				# lisfeatr = MySQLdb.escape_string(str(lisfeatr))
						# print type(lisfeatr)
						# print"@@@"
					# print lisfeatr
				break
			else:
				lisfeatr.append(a.text.encode('utf-8'))
				# lisfeatr = MySQLdb.escape_string(str(lisfeatr))
				# print a.text
	except:
		pass

	# print lisfeatr
else:
	lisfeatr.append("Sorry!!! no featured in")
	print lisfeatr
lisfeatr = MySQLdb.escape_string(str(lisfeatr))
print lisfeatr



######getting photos

photo = soup2.find_all("div",{"class":"row business-photos"})
# print photo[0]#.a.img['src']
# print "@@@@@@@@"
# print photo[0].find_all("img")
photolink= []
try:
	for img in photo[0].find_all("img"):
		# print img['src']
		photolink.append(img['src'])
	print photolink
except:
	photolink.append("No images found")
	print photolink

#done 

# featuredsm = soup2.find_all("ul",{"class":"expert-list"})
# print featuredsm[0].text
# prnt featured
# try:
	# for a in featuredsm:
	# 	for li_item in a.find_all("li"):
			# print li_item.text
			# print"@@@"
# except:
# 	print err
	# print a
	# print a.next_sibling
	# print "@@@@@"