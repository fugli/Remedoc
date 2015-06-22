from bs4 import BeautifulSoup
import re
import urllib2
import MySQLdb
import string
import requests
import json


def fn (url):
	req = urllib2.Request(url)
	html_page = urllib2.urlopen(req)#.read()
	soup = BeautifulSoup(html_page)
	# finalurl = html_page.geturl()
	return soup

alpha = list(string.ascii_uppercase)
# print alpha
print >> open('spec_qikwell.txt','w')," "
for letter in alpha:
	print letter
	url = 'http://www.qikwell.com/browse/specialities/'
	try:
		soup = fn (url+letter)
		specs_ul = soup.find('ul',{'id':'container-list'})
		specs_li = specs_ul.find_all('li')
		for item in specs_li:
			print >> open('spec_qikwell.txt','a')," ".join(item.text.encode('utf-8').split())

	except urllib2.HTTPError as err:
		print err.code
	except:
		continue
	# print specs_li