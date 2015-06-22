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

	sql = "select * from sheet3 where Body_part ="+'"'+name+'"'
	cursor.execute(sql)
	part_con_all = cursor.fetchall()
	
	for item in part_con_all:
		print item[1]
		sql = "select description from conditions where condition_name ="+'"'+item[2]+'"'
		# print sql
		cursor.execute(sql)
		desc = cursor.fetchone()
		desc = MySQLdb.escape_string(str(desc))
		sql1 = "INSERT INTO `sheet5`(`Body_part`, `conditions`, `description`) VALUES ("+'"'+name+'",'+'"'+str(item[2])+'",'+'"'+str(desc)+'"'+')'
		cursor.execute(sql1)
		db.commit()
		print name
	# sql_name = 'select Name from name_n_id where part_id = '+'"'+str(part_id)+'"'
	# cursor.execute(sql_name)