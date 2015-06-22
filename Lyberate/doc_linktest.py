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

###copy doc list in srcpg.html
def fn (url):
	html_page = urllib2.urlopen(url)
	soup = BeautifulSoup(html_page)
	return soup

soup = BeautifulSoup (open('srcpg.html'))
# print >>open('doc_url.txt','w'),''
# div_doc = soup.find('div',{'class':'span9'})
# div_doc_li = soup.find_all('div',{'class':'white_item'})
# print option
# print div_doc
# print div_doc_li
div_doc_li = soup.find_all('div',{'class':'name_block'})
for item in div_doc_li:
	# item= item.find('div',{'class':'name_block'})
	print item.a['href']
	print '########'
	# print >>open('city.txt','a'),item.a['href']