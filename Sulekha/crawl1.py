import requests            #from python lib
from bs4 import BeautifulSoup

# url = "http://yellowpages.sulekha.com/dental-surgeons-specialists_mumbai?utm_source=NG.sulekha.com&utm_medium=Search_suggest&utm_term=Dental%20Surgeons%20in%20Mumbai&utm_campaign=Search"
# req = requests.get(url)
# soup = BeautifulSoup(req.content)

import urllib2
import re

def fn (url):
	html_page = urllib2.urlopen(url)
	soup1 = BeautifulSoup(html_page)
	return soup1

# url = "http://yellowpages.sulekha.com/dental-surgeons-specialists_mumbai?utm_source=NG.sulekha.com&utm_medium=Search_suggest&utm_term=Dental%20Surgeons%20in%20Mumbai&utm_campaign=Search"
# html_page = urllib2.urlopen(url)
# soup = BeautifulSoup(html_page)
soup=fn("http://yellowpages.sulekha.com/dental-surgeons-specialists_mumbai?utm_source=NG.sulekha.com&utm_medium=Search_suggest&utm_term=Dental%20Surgeons%20in%20Mumbai&utm_campaign=Search")


f = open('outputcr.html', 'w')
# print >> open("output4.html","a"),soup.find_all("div", {"id":"listingtabcontent"})
# f.write(str(soup.find_all("div", {"id":"listingtabcontent"}))+"####")
div =  soup.find_all("div", {"id":"listingtabcontent"})

for item1 in div :
	# f.write(str(item1.find_all("li")))
	li = item1.find_all("li")
	# print type(li)
	for a in li:
		# f.write(str(a.find_all("a"))+'\n'+'##')
		# link = a.find_all("a")
		# f.write(str(link)+'\n'+'##')
		for link in a.find_all("a", {"class":"YPTRACK GAQ_C_BUSL"}):
			# f.write("http://yellowpages.sulekha.com"+str(link.get('href'))+'\n'+'\n')
			for href in link.get('href'):
				soup2 = fn("http://yellowpages.sulekha.com"+str(link.get('href')))
				f.write(str(soup2))
		# for link in a:

	# for item in item1:
		# f.write(str(item)+"#####" +'\n' )
		# for a in item.find_all("li", {"class":"list-item "}):
		# 	f.write(str(a.find_all("a"))+"#####" +'\n' )
