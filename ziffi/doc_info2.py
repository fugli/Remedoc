from bs4 import BeautifulSoup
import re
import urllib2
import MySQLdb
import string
import requests

# import socks
# import socket
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
# socket.socket = socks.socksocket


def fn (url):
	html_page = urllib2.urlopen(url)
	soup = BeautifulSoup(html_page)
	return soup

# soup1 = BeautifulSoup(open("htmlpgsrc2.html"))
soup1 = fn ('https://www.ziffi.com/doctors-in-mumbai/mona-kukreja-gynecology/')
doc_detail = {}

div_prof_photo = soup1.find("div",{"class":"profile-photo-block"}).img['src']
doc_detail.update({"div_prof_photo":div_prof_photo})


div_profcntanr = soup1.find("div",{"class":"profile-info-container"})
# print div_profcntanr

####name of the doc
h1tag_name = div_profcntanr.find("h1").text.encode('utf-8')
doc_detail.update({"h1tag_name":h1tag_name})
####deg of the doc
divtag_deg = div_profcntanr.find("div",{"class":["doctor-degrees" ,"text-line-ellipsis"]}).text.encode('utf-8')
doc_detail.update({"divtag_deg":divtag_deg})

#### brief infos
divtag_resele = div_profcntanr.find_all("div",{"class":"result-elements"})
spec = divtag_resele[0].text.encode('utf-8')
doc_detail.update({"spec":spec})

exp = divtag_resele[1].text.encode('utf-8')
doc_detail.update({"exp":exp})

# fees = divtag_resele[2].a['data-fees']
# doc_detail.update({"fees":fees})

####languages and fees
for div_item in divtag_resele:
	if div_item.find("a",{"class":"private-info-trigger"}):
		fees = div_item.a['data-fees']
		doc_detail.update({"fees":fees})

	elif div_item.find("i",{"class":"fa fa-language"}):
		spantag_lang = div_item.find_all("span")
		langs = []
		for item in spantag_lang:
			langs.append(item.text.encode('utf-8'))

		doc_detail.update({"langs":langs})
# print langs , fees,exp , spec
# print h1tag_name


div_blocks = soup1.find_all("div",{"class":"row section-block"})
# print div_blocks
spec_moreinfos = div_blocks[0].find("div",{"class":"small-9 medium-10 columns fade-container"}).text.encode('utf-8')
doc_detail.update({"spec_moreinfos":spec_moreinfos})

pos_moreinfos = div_blocks[0].find("div",{"class":"small-9 medium-10 columns fade-container doctor-position"}).text.encode('utf-8')
doc_detail.update({"pos_moreinfos":pos_moreinfos})
# avail_moreinfos = div_blocks[1].find("div",{"class":"small-9 medium-10 columns"})


for item in div_blocks[1:]:
	heading = item.find("h2",{"class" :"z-primary-color"}).text.encode('utf-8')

	if heading == "Photos":
		photo_link = []
		for li_photos in item.find_all("li",{"class":"gallery-item "}):   #thereis aspacechar
			photo_link.append(li_photos.img['src'])
		doc_detail.update({"photo_link":photo_link})
		# print photo_link

	elif heading == "Directions":
		# print "Directions"
		continue
		# div_map = item.find("div",{"id":"google-map"})
		# # print div_map
		# lat = div_map['data-lat']
		# lon = div_map['data-lng']
		# print lat,lon
	else:
		lists_heading = [] 
		for li_item in item.find_all("li",{"class":""}):
			lists_heading.append(li_item.text.encode('utf-8'))
		doc_detail.update({heading:lists_heading})
		# print heading
		# print lists_heading

print doc_detail


# print spec_moreinfos,pos_moreinfos


