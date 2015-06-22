from bs4 import BeautifulSoup
import re
import urllib2
import MySQLdb

db = MySQLdb.connect("localhost","root","8520","Docinfo")
cursor = db.cursor()


f = open('outputcr2.html', 'w')
def fn (url):
	html_page = urllib2.urlopen(url)
	soup1 = BeautifulSoup(html_page)
	return soup1

lis=[]
soup = BeautifulSoup(open("sulekha1.html"))
a=soup.find_all("div",{"class":"grid-block col3"},limit=3)
# print a[0].prettify()
href = a[0].find_all("a")
for a in href:
	lis.append(a.get('href'))


for link in lis[1:]:
	f.write(link+'\n')
	soup2=fn(link)
	div =  soup2.find_all("div", {"id":"listingtabcontent"})
	
	for item1 in div :
		li = item1.find_all("li" , {"class":"list-item "})
		for a in li:
			
			for link in a.find_all("a", {"class":"YPTRACK GAQ_C_BUSL"}):
				
				href1 = link.get('href')
				soup2 = fn("http://yellowpages.sulekha.com"+ href1 )

				f.write( href1 + "$$$$$$$$$$$$$$$$")
				
				divname = soup2.find_all("div",{"class":"pull-left"})
				divdesc = soup2.find_all("div",{"itemprop":"description"})
				lis2 = {"Phone/Mobile":"Not found","description":"Not found","pull-left":"Not found","Address":"Not found","Email":"Not found","Website":"Not found","Contact Person":"Not found","Working Hours":"Not found","Categories":"Not found"}

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

						# print "errrrrrrrrr1 ABOUT NOT FOUND"

				
				try:
					lis2.update({"pull-left" : divname[0].text.replace("'","\\'").encode('utf8') })

					# print "Clinic name :::",divname[0].h1.string
				except:
					print "errrrrrrr2"

				div2 = soup2.find_all("div",{"class":"profile-list"})
				for item in div2:
					 li2 = item.find_all("li",{"class":"row"})
					 for item2 in li2:
					 	dv1= item2.find_all("div",{"class":"profile-details"})
					 	dv2=item2.find_all("div",{"class":"profile-child"})
					 	
					 	for a in dv1:
					 		# print a.strong.text," ::: ", a.div.text
					 		lis2.update({a.strong.text.replace("'","\\'").encode('utf8') : " ".join(a.div.text.split()).replace("'","\\'").encode('utf8') })

				sql = "INSERT INTO `test`(`Phone`, `Address`, `Email`, `Website`, `Contact Person`, `Working hrs`, `Categories`,`About`, `Clinic name`) VALUES (" +"'" +lis2["Phone/Mobile"]+"'"+",'"+lis2["Address"]+"'"+",'"+lis2["Email"]+"'"+",'"+lis2["Website"]+"'"+",'"+lis2["Contact Person"]+"'"+",'"+lis2["Working Hours"]+"'"+",'"+lis2["Categories"]+"'"+",'"+lis2["description"]+"'"+",'"+lis2["pull-left"]+"'"+")"

				print sql
				cursor.execute(sql)
				db.commit()
					 		# f.write( str(a.strong.text)+" ::: " +str(a.div.text))
				print "########@@@@@@#####"
				# f.write("###############")



# print href