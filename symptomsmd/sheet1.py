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

# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
# socket.socket = socks.socksocket
# print >> open('filter.txt','w'),''

idd_filter = re.compile(r'[0-9]+')
sym_filter1 = re.compile(r'(^\(\')')
sym_filter2 = re.compile(r'(\',\)$)')

db = MySQLdb.connect("localhost","root","8520","symptoms_md")
cursor = db.cursor()

for part_id in range(1,100):
	part_id = str(part_id)
	sql = 'select distinct Symptom_ID from `Total_info2` where Part_ID = %s'%(part_id)
	cursor.execute(sql)
	res= cursor.fetchall ()
	for item in res:
		# print type(item)
		sym_id = idd_filter.search(str(item))
		
		sqlsymp = 'select Symp_Name from symptoms where Symp_ID = %s'%str(sym_id.group())
		cursor.execute(sqlsymp)
		sqlsymp = cursor.fetchone()
		sqlsymp = sym_filter1.sub('',str(sqlsymp))
		sqlsymp = sym_filter2.sub('',str(sqlsymp))
		# print >> open('filter.txt','a'),sym_id.group(),'@@@',sqlsymp,'@@@',part_id
		print part_id,sqlsymp
		sql_final = 'INSERT INTO `sheet1`(`Body_part`, `Related_symptoms`) VALUES ('+'"'+part_id+'",'+'"'+sqlsymp+'"'+')'
		cursor.execute(sql_final)
		db.commit()

# db.commit()
