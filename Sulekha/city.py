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

citylist=["mumbai","chennai","hyderabad","bangalore","delhi","kolkata","pune","ahmedabad","agra","allahabad"]
# soup = BeautifulSoup(open("sulekha1.html"))
# soup = BeautifulSoup(open("sulekha1.html"))
soupcity = BeautifulSoup(open("city.html"))

acity=soupcity.find_all("div",{"id":"defcity"})
# print a[0]
atag1 = acity[0].find_all("a")
# print atag1
liscity = []
for citi in atag1:
	# print citi.text.lower()
	liscity.append(citi.text.lower())
print len(liscity)

print liscity[48]





#test for replcing city in the list
# a=soup.find_all("div",{"class":"grid-block col3"},limit=3)


# href = a[0].find_all("a")
# for city in citylist:
# 	lis=[]
# 	for a in href:
# 		b= a.get('href')
# 		repcit=string.replace(b,'mumbai',city)
# 		lis.append(repcit)
		
# 	print lis,"\n"
		
		# print c
