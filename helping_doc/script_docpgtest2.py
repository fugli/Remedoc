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

# print >> open("clinics_bangalore_link.html",'a'),""
# print >> open("doc_bangalore_link.html",'a'),""
db = MySQLdb.connect("localhost","root","8520","Ziffi")
cursor = db.cursor()

def fn (url):
	req = urllib2.Request(url)
	html_page = urllib2.urlopen(req)#.read()
	soup = BeautifulSoup(html_page)
	finalurl = html_page.geturl()
	return [soup,finalurl]

TAG_RE = re.compile(r',*\xc2\xa0')

def remove_xc2(text):
	return TAG_RE.sub('', text)


soup2 = BeautifulSoup(open("src_pg.html"))

doc_link = soup2.find_all("a",{"class":"titel-01"})
for link in doc_link:
	print link['href']
print len(doc_link)

