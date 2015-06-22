from bs4 import BeautifulSoup
import re
import urllib2
import MySQLdb
import string
import requests

soup1 = BeautifulSoup(open("htmlpgsrc2.html"))

ul_popular = soup1.find("ul",{"class":"content-slider-ls no-bullet"})
li_popular = ul_popular.find_all("li")
for item_pop in li_popular:
	# print item_pop
	div_pop = item_pop.find("div",{"class":"doctor-brief-profile-container text-center"})
	doc_pop_url = div_pop.a['href']
	pop_rev = item_pop.find("div",{"class":"text-hover image-hover"})
	num_rev = pop_rev.text.encode('utf-8')
	try:
		star = len(pop_rev.find_all("span",{"class":"on"}))
	except:
		print "NO rev"
	print star,doc_pop_url,num_rev
