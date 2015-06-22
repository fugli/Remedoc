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
print >> open('symptom.txt','w'),''
url_sym = 'http://symptoms.webmd.com/scapp/SymptomCheckerAPI.svc/symptoms'
url_con = 'http://symptoms.webmd.com/scapp/SymptomCheckerAPI.svc/conditions'
url_sym_con = 'http://symptoms.webmd.com/scapp/SymptomCheckerAPI.svc/symptomsbycondition'

# item_age = 4
item_sex = 'M'
x = 2
# item_con = 10
idd_filter = re.compile(r'[0-9]+')
sql = 'select distinct Condition_ID from `conditions2`'
cursor.execute(sql)
res= cursor.fetchall ()
# con_id =10
part_id_list = []
age = [1,4,8,14,20,30,40,50,60,64]
print >> open('symptom.txt','w'),''
for item_age in age:
	for item in res:
		# print type(item)
		con_id = idd_filter.search(str(item))
		con_id = str(con_id.group())

		con_sym_body = json.dumps({"request":{"locale":"us","conditionid":con_id,"user":{"age":item_age,"gender":item_sex,"zip":"","vid":"1eea18c3-46e3-4c6b-a54f-1aa3ff800e1f"}}})
		r_con_sym= s.post(url=url_sym_con, data=con_sym_body)
		
		for item_con_sym in r_con_sym.json()['data']['symptoms']:
			# part_id = (item_con_sym['bps'])#['id']
			for item1 in item_con_sym['bps']:
				part_id = item1['id']
				if not part_id in part_id_list:
					part_id_list.append(part_id)
					part_nm = item1['nm']
			# part_name = item_con_sym['bps']['nm']

	# for item_con in (r_con.json()['data']['conditions']):
					# print item_age,part_id
					sql = 'INSERT INTO `name_n_id`(`Name`, `part_id`) VALUES ('+'"'+part_nm+'",'+'"'+str(part_id)+'"'+')'
					cursor.execute(sql)
					db.commit()
					print >> open('symptom.txt','a'),part_id,part_nm

				print item_age,part_id