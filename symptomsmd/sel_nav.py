from bs4 import BeautifulSoup
from selenium import webdriver
import re
import urllib2
import time
from selenium.webdriver.support.ui import Select
import string
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Firefox()
url = "http://symptoms.webmd.com/#symptomsView"
driver.get(url)

# html = driver.page_source
# soup = BeautifulSoup(html)
# print "soup.prettify()"
spec_box = driver.find_element_by_xpath("//select[@id='person-age']/option[@value='1']")
btn = driver.find_element_by_xpath("//button[@class='webmd-btn webmd-btn-pr webmd-btn-m']")
spec_box.click()
btn.click()
time.sleep(1)
# canvas = driver.find_element_by_xpath("//canvas[@id = 'bodymap-male']")
# canvas.click()
actions = ActionChains(driver)
canvas = driver.find_element_by_xpath("//canvas[@id = 'bodymap-male']")
drawing = ActionChains(driver)\
    .move_by_offset(560, 114)\
    .click(canvas)\
    .release()
drawing.perform()

# all_combi = open ("a","r").readlines()
# diction = {}
# i=1
# for item in all_combi:
# 	item = item.rstrip()
# 	if not diction.has_key(item):
# 		diction.update({"%s"%item:i})
# 		i = i + 1
# 	else:
# 		# print "repeated"
# 		continue
# # print >>open("combi_filtr_keys.txt","w"),diction.keys()
# all_combi =  diction.keys()

# for item in all_combi[:6]:
# 	item = item.rstrip()
# 	print item
# 	spec_box.clear()
# 	spec_box.send_keys(item)
# 	# driver.implicitly_wait(20)
# 	time.sleep(1)
# 	pgsrc = driver.page_source
# 	soup1 = BeautifulSoup(pgsrc)
# 	li_item = soup1.find_all('li',{"class":"ui-menu-item"})
# 	print li_item
# 	print "######"
# 	for item2 in li_item:
# 		print item2.find("span",{"class":"right"}).text
# 		print item2.find("a").text
# 		print "$$$$$$$$"


# driver.close()




