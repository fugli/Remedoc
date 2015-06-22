import urllib2;
from bs4 import BeautifulSoup;
import time;
import os;
import re;
import sys;
import urllib;
import requests
import json
import MySQLdb

db = MySQLdb.connect("localhost","root","8520","symptoms_md")
cursor = db.cursor()

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
       # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
       'Accept-Encoding': 'gzip, deflate',
       'Accept-Language': 'en-US,en;q=0.5',
      'Content-type': 'application/json; charset=utf-8',
      'Connection': 'keep-alive',
      'Referer':'http://symptoms.webmd.com/'}

s = requests.Session()
s.headers.update(hdr)

url_sym = 'http://symptoms.webmd.com/scapp/SymptomCheckerAPI.svc/symptoms'
url_con = 'http://symptoms.webmd.com/scapp/SymptomCheckerAPI.svc/conditions'
url_sym_con = 'http://symptoms.webmd.com/scapp/SymptomCheckerAPI.svc/symptomsbycondition'
print >> open('symptom.txt','w'),''
item_age = 4
item_sex = 'M'
x = 2
# item_sym['id'] = 
x = [2,2,2,41,44]
item_con = [869,858,887,359,437]
# item_con = 869

for item in item_con:
	con_sym_body = json.dumps({"request":{"locale":"us","conditionid":item,"user":{"age":item_age,"gender":item_sex,"zip":"","vid":"1eea18c3-46e3-4c6b-a54f-1aa3ff800e1f"}}})
	r_con_sym= s.post(url=url_sym_con, data=con_sym_body)
	symp_list = []
	for item_con_sym in r_con_sym.json()['data']['symptoms']:
		item_con_sym['nm'] = str(item_con_sym['nm']).encode('utf-8')
		item_con_sym['id'] = str(item_con_sym['id']).encode('utf-8')
		symp_list.append(item_con_sym['nm']+'$')
		symp_list.append(item_con_sym['id']+'$$')
	# body_con = json.dumps({"request":{"user":{"age":item_age,"gender":item_sex,"zip":"","vid":"1eea18c3-46e3-4c6b-a54f-1aa3ff800e1f"},"locale":"us","maxconditions":200,"bodyparts":[{"id":x,"symptoms":[{"id":item_sym['id'],"qclss":[]}]}]}})
	# r_con= s.post(url=url_con, data=body_con)
	print >> open('symptom.txt','a'),symp_list
# print sql