from bs4 import BeautifulSoup
import re
import urllib2


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
	print link
	soup2=fn(link)
	div =  soup2.find_all("div", {"id":"listingtabcontent"})
	
	for item1 in div :
		li = item1.find_all("li" , {"class":"list-item "})
		for a in li:
			
			for link in a.find_all("a", {"class":"YPTRACK GAQ_C_BUSL"}):
				
				href1 = link.get('href')
				soup2 = fn("http://yellowpages.sulekha.com"+ href1 )

				print href1 + "$$$$$$$$$$$$$$$$"
				
				divname = soup2.find_all("div",{"class":"pull-left"})
				divdesc = soup2.find_all("div",{"itemprop":"description"})
				try:
					if divdesc[0].p['id'] == "showmore":
						print divdesc[0].contents[1].p.contents[0]
					else:
						print "About :::",divdesc[0].p.text	
				except:
					try:
						print "About :::",divdesc[0].contents[0]
					except:
						print "errrrrrrrrr1 ABOUT NOT FOUND"

				
				try:
					print "Clinic name :::",divname[0].h1.string
				except:
					print "errrrrrrr2"

				div2 = soup2.find_all("div",{"class":"profile-list"})
				for item in div2:
					 li2 = item.find_all("li",{"class":"row"})
					 for item2 in li2:
					 	dv1= item2.find_all("div",{"class":"profile-details"})
					 	dv2=item2.find_all("div",{"class":"profile-child"})
					 	
					 	for a in dv1:
					 		print a.strong.text," ::: ", a.div.text

					 		# f.write( str(a.strong.text)+" ::: " +str(a.div.text))
				print "########@@@@@@#####"
				# f.write("###############")



# print href