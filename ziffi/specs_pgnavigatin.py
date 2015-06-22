from bs4 import BeautifulSoup
from selenium import webdriver
import re
import urllib2
import time
from selenium.webdriver.support.ui import Select
import string

browser = webdriver.Firefox()
url = "https://www.ziffi.com/doctors-in-hyderabad/"
browser.get(url)

html = browser.page_source
soup = BeautifulSoup(html)
print "soup.prettify()"
spec_box = browser.find_element_by_class_name("ui-autocomplete-input")


# all_combi = open ("combi_filtr_keys.txt","r").readlines()
# # all_combi =  all_combi[0]
# print len(all_combi)


all_combi = open ("a","r").readlines()
diction = {}
i=1
for item in all_combi:
	item = item.rstrip()
	if not diction.has_key(item):
		diction.update({"%s"%item:i})
		i = i + 1
	else:
		# print "repeated"
		continue
# print >>open("combi_filtr_keys.txt","w"),diction.keys()
all_combi =  diction.keys()

for item in all_combi[:6]:
	item = item.rstrip()
	print item
	spec_box.clear()
	spec_box.send_keys(item)
	# browser.implicitly_wait(20)
	time.sleep(1)
	pgsrc = browser.page_source
	soup1 = BeautifulSoup(pgsrc)
	li_item = soup1.find_all('li',{"class":"ui-menu-item"})
	print li_item
	print "######"
	for item2 in li_item:
		print item2.find("span",{"class":"right"}).text
		print item2.find("a").text
		print "$$$$$$$$"


browser.close()





# alpha = list(string.ascii_lowercase)
# alpha = ['']+alpha
# print alpha
# for l1 in alpha[1:]:
# 	for l2 in alpha:
# 		for l3 in alpha:
# 			for l4 in alpha:
# 				text = l1 + l2 + l3 + l4
# 				print >> open("aplha_comb.txt","a"),text
	
