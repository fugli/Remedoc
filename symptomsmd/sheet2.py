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
	symp_id_list= cursor.fetchall ()
	for item in symp_id_list:
		print type(item)
		s_id = idd_filter.search(str(item))
		s_id = s_id.group()
		sqlsymp = 'select Symp_Name from symptoms where Symp_ID = %s'%str(s_id)
		cursor.execute(sqlsymp)

		symp_name = cursor.fetchone()
		symp_name = sym_filter1.sub('',str(symp_name))
		symp_name = sym_filter2.sub('',str(symp_name))
		# print >> open('filter.txt','a'),s_id,'@@@',symp_name,'@@@',part_id

		sqlcond_id = 'select distinct Condition_ID from Total_info2 where Part_ID =%s and Symptom_ID =%s'%(part_id,str(s_id))
		cursor.execute(sqlcond_id)
		cond_id_list= cursor.fetchall ()

		for item_cid in cond_id_list:
			c_id = idd_filter.search(str(item_cid))
			c_id = c_id.group()
			sql_cname = 'select condition_name from conditions2 where condition_ID =%s'%str(c_id)
			cursor.execute(sql_cname)
			cond_name = cursor.fetchone()
			cond_name = sym_filter1.sub('',str(cond_name))
			cond_name = sym_filter2.sub('',str(cond_name))
			# print >> open('filter.txt','a'),cond_name,'####'
			symp_name = MySQLdb.escape_string(symp_name)
			cond_name = MySQLdb.escape_string(cond_name)
			print part_id,symp_name,cond_name
			sql_f = 'INSERT INTO `Sheet2`( `Body_part`,`Related_symptom`, `Conditions`) VALUES ('+'"'+part_id+'",'+'"'+symp_name+'",'+'"'+cond_name+'"'+')'
			cursor.execute(sql_f)
			db.commit()
			print '####'
