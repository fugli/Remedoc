from bs4 import BeautifulSoup
from selenium import webdriver
import re
import urllib2
import time
from selenium.webdriver.support.ui import Select
import string

browser = webdriver.Firefox()
url = "https://www.helpingdoc.com/"
browser.get(url)

html = browser.page_source
soup = BeautifulSoup(html)
print "soup.prettify()"
spec_box = browser.find_element_by_id("searchTextBox")

alpha = list(string.ascii_lowercase)
# all_combi = open ("combi_filtr_keys.txt","r").readlines()
# # all_combi =  all_combi[0]
# print len(all_combi)
print alpha

regex_obj = re.compile(r'\(.+\)')

print >>open ("specs_hel_doc.txt",'w'),""

for item in alpha:
	print item
	spec_box.clear()
	spec_box.send_keys(item)
	# browser.implicitly_wait(20)
	time.sleep(2)
	pgsrc = browser.page_source
	soup1 = BeautifulSoup(pgsrc)
	li_item = soup1.find_all('li',{"class":"ui-menu-item"})
	for item_li in li_item:
		specs = item_li.text
		print specs
		if not re.search(regex_obj,specs):
			print "Iamin"
			spec_file = open('specs_hel_doc.txt','r').readlines()
			# print spec_file
			if not str(specs) + '\n' in spec_file:
				print "#################################"
				print >>open ("specs_hel_doc.txt",'a'),specs
	print "@@@@@@@@@@@@@@"
		

browser.close()

spec_file = open('specs_hel_doc.txt','r').readlines()
if ("ent specialist"+'\n') in spec_file:
	print "true"



# alpha = list(string.ascii_lowercase)
# alpha = ['']+alpha
# print alpha
# for l1 in alpha[1:]:
# 	for l2 in alpha:
# 		for l3 in alpha:
# 			for l4 in alpha:
# 				text = l1 + l2 + l3 + l4
# 				print >> open("aplha_comb.txt","a"),text
	
