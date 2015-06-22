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

# for part_id in range(1,100):
# 	part_id = str(part_id)
# 	sql = 'select distinct Condition_ID from `Total_info2` where Part_ID = %s'%(part_id)
# 	cursor.execute(sql)
# 	res= cursor.fetchall ()
# 	for item in res:
# 		# print type(item)
# 		con_id = idd_filter.search(str(item))
# 		if con_id.group() == '1216':
# 			print 'continue'
# 			continue

sqlsymp = 'select * from conditions2' #where condition_ID = %s'%str(con_id.group())
cursor.execute(sqlsymp)
cond_data1 = cursor.fetchall()
# try:
for cond_data in cond_data1: 
	c_s_list = re.findall(r'([A-Za-z\s\(\)]+\$)',cond_data[3])
	c_s_list = rem_dol.sub('',str(c_s_list))


	data = []
	for i in range(4,16):
		data.append(remove_xc2(remove_tags(cond_data[i])))

	for i in range(0,12):
		data[i] =  MySQLdb.escape_string(str(data[i]))


	sql_con1 = "INSERT INTO `conditions`(`condition_name`, `condition_ID`, `symptomsbycondition`,"
	sql_con2 = "`description`, `what_to_expect`, `how_common`, `did_you_know`, `made_worse_by`, `how_its_diagnosed`,"
	sql_con3 = "`questions_to_ask_your_dr`, `treatment`, `self_care`, `risk_factors`, `when_to_see_a_doctor`, `fact`) VALUES ("
	sql_con4 = '"'+cond_data[1]+'",'+'"'+cond_data[2]+'",'+'"'+str(c_s_list)+'",'+'"'+data[0] +'",'
	sql_con5 = '"'+data[1]+'",'+'"'+data[2]+'",'+'"'+data[3]+'",'+'"'+data[4]+'",'+'"'+data[5]+'",'
	sql_con6 = '"'+data[6]+'",'+'"'+data[7]+'",'+'"'+data[8]+'",'+'"'+data[9]+'",'
	sql_con7 = '"'+data[10]+'",'+'"'+data[11]+'"'+')'
	sql_con = sql_con1 + sql_con2+sql_con3+sql_con4+sql_con5+sql_con6+sql_con7 
	# print sql_con
	cursor.execute(sql_con)
	db.commit()
	print '####',cond_data[1]

	# db.commit()
