from bs4 import BeautifulSoup
import re
import urllib2
import MySQLdb
import string
import requests
from selenium import webdriver
import json
import socks
import socket


db = MySQLdb.connect("localhost","root","8520","symptoms_md")
cursor = db.cursor()
sym_filter2 = re.compile(r'(\',\)$)')
sym_filter1 = re.compile(r'(^\(\')')
print >> open('filter.txt','w'),''
for part_id in range(1,69):

	sql_name = 'select Name from name_n_id where part_id = '+'"'+str(part_id)+'"'
	cursor.execute(sql_name)
	name = cursor.fetchone()
	name = sym_filter1.sub('',sym_filter2.sub('',str(name)))
	# print >> open('filter.txt','a'),name,part_id
	print name,part_id
	sqlupdate = "update sheet3 set Body_part ="+'"'+str(name)+'"'+" where Body_part ="+'"'+str(part_id)+'"'
	# print sqlupdate
	cursor.execute(sqlupdate)
	db.commit()
	print '###'
 