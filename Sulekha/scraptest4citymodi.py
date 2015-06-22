from bs4 import BeautifulSoup
import re
import urllib2
import MySQLdb
import string

db = MySQLdb.connect("localhost","root","8520","Docinfo")
cursor = db.cursor()


f = open('outputcr2.html', 'w')
def fn (url):
	html_page = urllib2.urlopen(url)
	soup1 = BeautifulSoup(html_page)
	return soup1


soup = BeautifulSoup(open("sulekha1.html"))
a=soup.find_all("div",{"class":"grid-block col3"},limit=3)
# liscity=["mumbai","chennai","hyderabad","bangalore","delhi","kolkata","pune","ahmedabad","agra","allahabad"]

soupcity = BeautifulSoup(open("city.html"))
acity=soupcity.find_all("div",{"id":"defcity"})
atag1 = acity[0].find_all("a")
liscity = []
for citi in atag1:
	# print citi.text.lower()
	liscity.append(citi.text.lower().encode('utf-8'))
# print liscity
# print len(liscity)

# print liscity[48]

# print a[0].prettify()
href = a[0].find_all("a")
for city in liscity:
	# print city
	lis=[]
	for a in href:
		b= a.get('href')
		repcit=string.replace(b,'mumbai',city)
		repcit=repcit.encode('utf-8')
		lis.append(repcit)
	# print lis
# for a in href:
# 	lis.append(a.get('href'))


	for link1 in lis[1:]:
		# for n in range(1,200):
		# 	link1=link1+"_"+n
		# 	if di

		# print link1
		
		# soup2=fn(link1)
		soup2=fn("http://yellowpages.sulekha.com/cardiologists-cardiology-clinics_mumbai_200")
		div =  soup2.find_all("div", {"id":"listingtabcontent"})
		print div

		try:
			print "Im in try"
			for item1 in div :
				li = item1.find_all("li" , {"class":"list-item "})
				print li
				for a in li:
					
					for link in a.find_all("a", {"class":"YPTRACK GAQ_C_BUSL"}):
						
						href1 = link.get('href')
						soup2 = fn("http://yellowpages.sulekha.com"+ href1 )
						# print href1 

						
						# f.write( href1 + "$$$$$$$$$$$$$$$$"+'\n')
						
						ratingtot= soup2.find_all("div" , {"class":"span6"})
						divname = soup2.find_all("div",{"class":"pull-left"})
						divdesc = soup2.find_all("div",{"itemprop":"description"})
						lis2 = {"Link":"Not found","Link sec":"Not found","Phone/Mobile":"Not found","description":"Not found","pull-left":"Not found","Address":"Not found","Email":"Not found","Website":"Not found","Contact Person":"Not found","Working Hours":"Not found","Categories":"Not found"}
						
						#####getting overall rating info
						lisdic = {"ratingtot": "not found","review": "not found","usrrate": "not found","name": "not found","docname": "not found","link": "not found","badge": "not found"}
						try:
							lisdic.update({"ratingtot":ratingtot[0].text.encode('utf-8')})
						except:
							lisdic.update({"ratingtot":"Not found"})
							pass

						lisdic["ratingtot"]= MySQLdb.escape_string(str(lisdic["ratingtot"]))


						######getting badge info
						badge = soup2.find_all("div",{"class":"manage-prolink"})
						try:
							lisdic.update({"badge":badge[0].span['class'][1]})
							# print lisdic["badge"]
						except:
							lisdic.update({"badge":"Sorry !! badge not found"})

						lisdic["badge"]=MySQLdb.escape_string(str(lisdic["badge"]))


						#updating the link used in retrieving data
						lis2.update({"Link" : link1})
						lis2.update({"Link sec" : href1})

						#####for getting About info 
						try:
							if divdesc[0].p['id'] == "showmore":
								lis2.update({"description" : divdesc[0].contents[1].p.text.replace("'","\\'").encode('utf8')})
								# print divdesc[0].contents[1].p.contents[0]
							else:
								lis2.update({"description" : divdesc[0].p.text.replace("'","\\'").encode('utf8')})

								# print "About :::",divdesc[0].p.text	
						except:
							try:
								lis2.update({"description" : divdesc[0].text.replace("'","\\'").encode('utf8')})

								# print "About :::",divdesc[0].contents[0]
							except:
								lis2.update({"description" : "errrrrrrrrr1 ABOUT NOT FOUND"})

						lis2["description"] = MySQLdb.escape_string(str(lis2["description"]))
								# print "errrrrrrrrr1 ABOUT NOT FOUND"

						####getting clinic name info
						try:
							lis2.update({"pull-left" : divname[0].text.replace("'","\\'").encode('utf8') })

							# print "Clinic name :::",divname[0].h1.string
						except:
							lis2.update({"pull-left" : "errrrrrrr2" })
							# print "errrrrrrr2"
						lis2["pull-left"] = MySQLdb.escape_string(str(lis2["pull-left"]))

						####getting photos
						photo = soup2.find_all("div",{"class":"row business-photos"})
						# print photo[0]#.a.img['src']
						# print "@@@@@@@@"
						# print photo[0].find_all("img")
						photolink= []
						try:
							for img in photo[0].find_all("img"):
								# print img['src']
								photolink.append(img['src'])#.replace("'","\\'"))
							# print photolink
							# photolink = MySQLdb.escape_string(str(photolink))
						except:
							photolink.append("No images found")
							# photolink = MySQLdb.escape_string(str(photolink))
							# print photolink

						photolink = MySQLdb.escape_string(str(photolink))

						# #####getting featured in
						# lisfeatr = []
						# featured=soup2.find_all("span",{"class":"featured"})
						# if featured:
						# 	atag= featured[0].find_all("a")
						# 	# print atag
						# 	try:
						# 		for a in atag:
						# 			if(a['href']=="#prdservice"):
						# 				featuredsm = soup2.find_all("ul",{"class":"expert-list"})
						# 				# print featuredsm
						# 				for a in featuredsm:
						# 					for li_item in a.find_all("li"):
						# 						# print li_item.text
						# 						lisfeatr.append(li_item.text.encode('utf-8'))
						# 						lisfeatr = MySQLdb.escape_string(str(lisfeatr))

						# 						# print"@@@"
						# 				break
						# 			else:
						# 				lisfeatr.append(a.text.replace("'","\\'").encode('utf-8'))
						# 				lisfeatr = MySQLdb.escape_string(str(lisfeatr))
						# 				# print a.text
						# 	except:
						# 		pass

						# 	# print lisfeatr
						# else:
						# 	lisfeatr.append("Sorry!!! no featured in".replace("'","\\'"))
						# 	lisfeatr = MySQLdb.escape_string(str(lisfeatr))
						# 	# print lisfeatr


						######to find featured In of doc
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
							# print lisfeatr
						
						lisfeatr = MySQLdb.escape_string(str(lisfeatr))
						# print lisfeatr




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
									usrlis.append(" ".join(revpar[0].p.text.split()).encode('utf-8'))
									usrlis.append(" ".join(revpar[0].div.span.text.split()).encode('utf-8'))
									usrlis.append(" ".join(revpar[0].h3.text.split()).encode('utf-8'))
									# print us)rlis
									lisusrlis.append(usrlis)
								# print lisusrlis
								# print "@@@@@@@@@@@"
								# strList = MySQLdb.escape_string(str(lisusrlis))
								# print strList
								# strList.replace('"','\\"')
								# strList.replace("'","\'")
									# print usrlis
									# print "@@@@@@"+'\n'
								# print lisusrlis
								# print "$$$$$$$"
							except:
								lisusrlis.append("SORRY!! ")
								# print lisusrlis
						else:
							lisusrlis.append("SORRY!! no reviews were found ")
							# print lisusrlis

						strList = MySQLdb.escape_string(str(lisusrlis))


						#####getting phone,website,contact,email etc
						div2 = soup2.find_all("div",{"class":"profile-list"})
						for item in div2:
							 li2 = item.find_all("li",{"class":"row"})
							 for item2 in li2:
							 	dv1= item2.find_all("div",{"class":"profile-details"})
							 	dv2=item2.find_all("div",{"class":"profile-child"})
							 	
							 	for a in dv1:
							 		# print a.strong.text," ::: ", a.div.text
							 		try:
							 			lis2.update({a.strong.text.replace("'","\\'").encode('utf8') : " ".join(a.div.text.split()).replace("'","\\'").encode('utf8') })


							 		except:
							 			lis2.update({a.strong.text.replace("'","\\'").encode('utf8') : "err bro"})


						lis2["Phone/Mobile"] = MySQLdb.escape_string(str(lis2["Phone/Mobile"]))
						lis2["Address"] = MySQLdb.escape_string(str(lis2["Address"]))
						lis2["Email"] = MySQLdb.escape_string(str(lis2["Email"]))
						lis2["Website"] = MySQLdb.escape_string(str(lis2["Website"]))
						lis2["Contact Person"] = MySQLdb.escape_string(str(lis2["Contact Person"]))
						lis2["Working Hours"] = MySQLdb.escape_string(str(lis2["Working Hours"]))
						lis2["Categories"] = MySQLdb.escape_string(str(lis2["Categories"]))

						sql = "INSERT INTO `test`(`Phone`, `Address`, `Email`, `Website`, `Contact Person`, `Working hrs`, `Categories`,`About`, `Clinic name`, `Link`, `Link sec`, `City`,`Badge`, `Photoslink`, `Reviews`, `Featuredin`, `RatingTot`) VALUES (" +'"' +lis2["Phone/Mobile"]+'"'+',"'+lis2["Address"]+'"'+',"'+lis2["Email"]+'"'+',"'+lis2["Website"]+'"'+',"'+lis2["Contact Person"]+'"'+',"'+lis2["Working Hours"]+'"'+',"'+lis2["Categories"]+'"'+',"'+lis2["description"]+'"'+',"'+lis2["pull-left"]+'"'+',"'+lis2["Link"]+'"'+',"'+lis2["Link sec"]+'"'+',"'+city+'"'+',"'+lisdic["badge"]+'"'+',"'+str(photolink)+'"'+',"'+str(strList)+'"'+',"'+str(lisfeatr)+'"'+',"'+lisdic["ratingtot"]+'"'+ ")"

						# print sql
						cursor.execute(sql)
						db.commit()
						# print lis2["Link"]
						print lis2["Link sec"]
							 		# f.write( str(a.strong.text)+" ::: " +str(a.div.text))
						print "########@@@@@@#####"
						# f.write("###############")

		except:
			flag = 1
			print "exception"
			pass



	# print href