import requests            #from python lib
from bs4 import BeautifulSoup

url = "http://yellowpages.sulekha.com/dental-surgeons-specialists_mumbai?utm_source=NG.sulekha.com&utm_medium=Search_suggest&utm_term=Dental%20Surgeons%20in%20Mumbai&utm_campaign=Search"
req = requests.get(url)
soup = BeautifulSoup(req.content)

# print >> open("output","w")
# print >> open("output2","w")
# print >> open("output3.html","w")
# print >> open("output","a"),soup.prettify().encode('utf8')
# print >> open("output2","a"),soup.find_all("div")
# print >> open("output3.html","a"),soup.find_all("div", {"id":"listing","class":"navigation"}).contents[0].contents[0]
# print >> open("output3.html","a"),soup.find_all("div", {"id":"listingtabcontent"})

for item in soup.find_all("div", {"id":"listingtabcontent"}): 
	# print >> open("output3.html","a"),item.find_all("li" , {"class":"list-item"}).contents ,"#########"

	f = open('output3.html', 'w')
	for li_item in item.find_all("li" , {"class":"list-item"}):
		# print type(li_item)#.contents[1].text)
		f.write(str(li_item.contents[1].text )+'\n' )
		# print >> open("output3.html","a"),item.contents ,"#########"

