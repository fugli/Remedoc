import requests            #from python lib
from bs4 import BeautifulSoup


import urllib2
import re

def fn (url):
	html_page = urllib2.urlopen(url)
	soup1 = BeautifulSoup(html_page)
	return soup1


soup=fn("http://yellowpages.sulekha.com/dental-surgeons-specialists_mumbai?utm_source=NG.sulekha.com&utm_medium=Search_suggest&utm_term=Dental%20Surgeons%20in%20Mumbai&utm_campaign=Search")


f = open('outputcr2.html', 'w')
div =  soup.find_all("div", {"id":"listingtabcontent"})

for item1 in div :
	li = item1.find_all("li")
	for a in li:
		
		for link in a.find_all("a", {"class":"YPTRACK GAQ_C_BUSL"}):
			# f.write(str(link.get('href'))+'\n')
			# print type(link.get('href'))
			href = link.get('href')
			soup2 = fn("http://yellowpages.sulekha.com"+ href )
				# f.write(str(soup2))
			# f.write(str(soup2.find_all("div",{"class":"profile-list"})) +'\n'+'\n'+"######")
			div2 = soup2.find_all("div",{"class":"profile-list"})
			for item in div2:
				 # f.write(str(item.find_all("li",{"class":"row"})) +'\n'+'\n'+"######")
				 li2 = item.find_all("li",{"class":"row"})
				 # print li2[0].contents
				 for item2 in li2:
				 	# f.write(str(item2)+'\n'+'\n')
				 	dv1= item2.find_all("div",{"class":"profile-details"})
				 	dv2=item2.find_all("div",{"class":"profile-child"})
				 	print dv1,"##############"
				 	print type(dv1)
				 	f.write(str( dv1[0].contents[0].contents[0])+'\n')
				 	print dv2[0].contents[0]
				 	# f.write( str(dv2[0].contents[0].contents[0])+'\n')

				 	# for item3 in item2.contents:
				 		# f.write(str(item3.find_all("div",{"class":"profile-details"})))
				 		# dv2=item3.find_all("div",{"class":"profile-child"})
				 		# # f.write(dv1.contents+":"+dv2.contents+'\n'+'\n')
				 		# print dv1,dv2

				 	# print type (item2.contents)
				 # f.write(li2[0].contents+'\n')
				 # for li_item in li2:
				 	# f.write((li_item.find_all("div")) +'\n')
				 	# for item2 in li_item.find_all("div"):
				 	# 	f.write(item2.contents+'\n')

				 f.write('                       '+"##############################################################################"+'\n')

		
