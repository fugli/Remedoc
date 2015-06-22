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
print >> open('filter.txt','w'),''

idd_filter = re.compile(r'[0-9]+')
sym_filter1 = re.compile(r'(^\(\')')
sym_filter2 = re.compile(r'(\',\)$)')

rem_dol = re.compile(r'[$(<.+>)]')
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
	return TAG_RE.sub('', text)
xc_rem = re.compile(r',*\xc2\xa0')
def remove_xc2(text):
	return xc_rem.sub('', text)

db = MySQLdb.connect("localhost","root","8520","symptoms_md")
cursor = db.cursor()

for part_id in range(1,100):
	part_id = str(part_id)
	sql = 'select distinct Condition_ID from `Total_info2` where Part_ID = %s'%(part_id)
	cursor.execute(sql)
	res= cursor.fetchall ()
	for item in res:
		# print type(item)
		con_id = idd_filter.search(str(item))
		if con_id.group() == '1216':
			print 'continue'
			continue
		
		sqlsymp = 'select * from conditions2 where condition_ID = %s'%str(con_id.group())
		cursor.execute(sqlsymp)
		cond_data = cursor.fetchone()
		# try:
		c_s_list = re.findall(r'([A-Za-z\s\(\)]+\$)',cond_data[3])
		c_s_list = rem_dol.sub('',str(c_s_list))

		# cond_data[3] = c_s_list
		# data = []
		# for i in range(4,16):
		# 	data.append(remove_xc2(remove_tags(cond_data[i])))
		# print >> open('filter.txt','a'),c_s_list,'@@@',cond_data[1]#,cond_data[3]
		# except:
		# 	print 'err',cond_data,con_id.group(),part_id
		# 	print  >> open('filter.txt','a'),cond_data
		# sqlsymp = sym_filter1.sub('',str(sqlsymp))
		# sqlsymp = sym_filter2.sub('',str(sqlsymp))
		# print >> open('filter.txt','a'),con_id.group(),'@@@',sqlsymp,'@@@',part_id
		# print part_id,sqlsymp
		
		####uncomment below portion not above
		sql_final = 'INSERT INTO `sheet3`(`Body_part`, `Conditions`, `symptomsbycondition`) VALUES ('+'"'+part_id+'",'+'"'+str(cond_data[1])+'",'+'"'+str(c_s_list)+'"'+')'
		cursor.execute(sql_final)
		db.commit()
		print '####',part_id

# db.commit()
