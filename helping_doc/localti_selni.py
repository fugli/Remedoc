###this is for getting locality of all cities in helping doc`
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import urllib2
import time
from selenium.webdriver.support.ui import Select

browser = webdriver.Firefox()
url = "https://www.helpingdoc.com/"
browser.get(url)

html = browser.page_source
soup = BeautifulSoup(html)
print "soup.prettify()"

# T_box = browser.find_element_by_id('searchTextBox')#.click()
# T_box.send_keys("yourInfoHere")  ##for writing text in a text box
drop_box = browser.find_element_by_id("CityDropdown")
dropdown =  Select(drop_box)

srcpage = open("src_pg.html","r")
soup1 = BeautifulSoup (srcpage)
atag = soup.find_all("option")
city=[]
for item in atag:
	city.append(" ".join(item.text.encode('utf-8').split()))



for item in city:
	
	dropdown.select_by_visible_text(str(item))
	time.sleep(50)
	print "line 34"
	soup2 = BeautifulSoup(browser.page_source)
	sel_tags = soup2.find("select",{"id":"AreaDropdown"})
	for option in sel_tags.find_all("option"):
		print >> open ("%s locality.txt"%str(item),"a")," ".join(option.text.encode('utf-8').split())
	
	print "@@@@@@@@@@@@@@@@@@@@@@"+'\n'
browser.close()


