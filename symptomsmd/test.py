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

# def fndata(key,data):
# 	try:
# 		key =  data[key]['#cdata-section'].encode('utf-8')
# 	except:
# 		key = 'NF'
# 	return key

# key_list = ['condition_description','what_to_expect','how_common','did_you_know','made_worse_by']
# key_list.extend(['how_its_diagnosed','questions_to_ask_your_dr','treatment','self_care','risk_factors'])
# key_list.extend(['when_to_see_a_doctor','fact'])
com_id_list = []
print >> open('symptom.txt','w'),''
print >> open('output.txt','w') , ''
age = [1,4,8,14,20,30,40,50,60,64]
sex = ['M','F']
for item_sex in sex:
	print item_sex
	for item_age in age:
		print item_age,'#######'
		for x in range(1,100):
			print x
			body_sym = json.dumps({"request":{"user":{"age":item_age,"gender":item_sex,"zip":"","vid":"1eea18c3-46e3-4c6b-a54f-1aa3ff800e1f"},"locale":"us","bodypartid":x}})
			# print body_sym
			r_sym= s.post(url=url_sym, data=body_sym)

			# print >> open('symptom.txt','a'),r_sym.content
			
			for item_sym in r_sym.json()['data']['symptoms']:
				item_sym['nm'] = str(item_sym['nm']).encode('utf-8')
				item_sym['id'] = str(item_sym['id']).encode('utf-8')
				# print >> open('symptom.txt','a'),item_sym['nm'],item_sym['id'], "&&&&&&"

				body_con = json.dumps({"request":{"user":{"age":item_age,"gender":item_sex,"zip":"","vid":"1eea18c3-46e3-4c6b-a54f-1aa3ff800e1f"},"locale":"us","maxconditions":200,"bodyparts":[{"id":x,"symptoms":[{"id":item_sym['id'],"qclss":[]}]}]}})
				r_con= s.post(url=url_con, data=body_con)
				# print r_con.json()['data']['conditions']
				
				####getting conditions
				for item_con in (r_con.json()['data']['conditions']):
				
					####storing conditions in conditios table
					item_con['name'] = str(item_con['name']).encode('utf-8')
					item_con['id'] = str(item_con['id']).encode('utf-8')
					item_con['conchronid'] = str(item_con['conchronid']).encode('utf-8')
					
					print item_con['name'],item_con['id'],item_con['conchronid'],item_sym['nm'],"*******",item_age,item_sex,x

					if not item_con['id'] in com_id_list and item_con['conchronid'] :
						symp_list = []
						data_list = []
						com_id_list.append(item_con['id'])
						# print >> open('symptom.txt','a'),item_con['name'],item_con['id']
						# print sql
						####getting sympton of this condition
						con_sym_body = json.dumps({"request":{"locale":"us","conditionid":item_con['id'],"user":{"age":item_age,"gender":item_sex,"zip":"","vid":"1eea18c3-46e3-4c6b-a54f-1aa3ff800e1f"}}})
						r_con_sym= s.post(url=url_sym_con, data=con_sym_body)

						for item_con_sym in r_con_sym.json()['data']['symptoms']:
							item_con_sym['nm'] = str(item_con_sym['nm']).encode('utf-8')
							item_con_sym['id'] = str(item_con_sym['id']).encode('utf-8')
							symp_list.append(item_con_sym['nm']+'$')
							symp_list.append(item_con_sym['id']+'$$')
						# print  >> open('output.txt','a'),symp_list
						symp_list = MySQLdb.escape_string(str(symp_list))
						####getting info of the webpg
						urlpg = 'http://symptoms.webmd.com/scapp/SymptomCheckerArticle.svc/article/'+item_con['conchronid']
						# print urlpg
						print item_con['name'],item_con['id'],item_con['conchronid'],item_sym['nm']
						web_pg = s.get(urlpg)
						json_content = web_pg.json()
						# json_content = json.loads(web_pg.content)
						# a = web_pg.content["webmd_rendition"]#["content"]["wbmd_asset"]["metadata_section"]
						data = (json_content["webmd_rendition"]["content"]["wbmd_asset"]["content_section"]["cons_symptom_checker"])
						
					
						try:condition_description = MySQLdb.escape_string(data['condition_description']['#cdata-section'].encode('utf-8'))
						except:condition_description = 'NF'
						try:what_to_expect = MySQLdb.escape_string (data['what_to_expect']['#cdata-section'].encode('utf-8'))
						except:what_to_expect ='Nf'
						try:how_common = MySQLdb.escape_string(data['how_common']['#cdata-section'].encode('utf-8'))
						except:how_common ='Nf'
						try:did_you_know = MySQLdb.escape_string(data['did_you_know']['#cdata-section'].encode('utf-8'))
						except:did_you_know = 'Nf'
						try:made_worse_by = MySQLdb.escape_string(data['made_worse_by']['#cdata-section'].encode('utf-8'))
						except:made_worse_by = 'Nf'
						try:how_its_diagnosed = MySQLdb.escape_string(data['how_its_diagnosed']['#cdata-section'].encode('utf-8'))
						except:how_its_diagnosed = 'Nf'
						try:questions_to_ask_your_dr =MySQLdb.escape_string( data['questions_to_ask_your_dr']['#cdata-section'].encode('utf-8'))
						except:questions_to_ask_your_dr ='Nf'
						try:treatment = MySQLdb.escape_string(data['treatment']['#cdata-section'].encode('utf-8'))
						except:treatment ='Nf'
						try:self_care = MySQLdb.escape_string(data['self_care']['#cdata-section'].encode('utf-8'))
						except:self_care ='Nf'
						try:risk_factors = MySQLdb.escape_string(data['risk_factors']['#cdata-section'].encode('utf-8'))
						except:risk_factors ='Nf'
						try:when_to_see_a_doctor = MySQLdb.escape_string(data['when_to_see_a_doctor']['#cdata-section'].encode('utf-8'))
						except:when_to_see_a_doctor ='Nf'
						try:fact = MySQLdb.escape_string(data['fact']['#cdata-section'].encode('utf-8'))
						except:fact = 'Nf'
						
						# print >> open('output.txt','a'),description
						# print >> open('output.txt','a'),data_list

						# print >> open('output.txt','w'),(json_content)

						# out = open('data.txt', 'wt')
						# print json.dump(web_pg.json()["webmd_rendition"]["content"]["wbmd_asset"], out)
						sql_con1 = "INSERT INTO `conditions2`(`condition_name`, `condition_ID`, `symptomsbycondition`,"
						sql_con2 = "`description`, `what_to_expect`, `how_common`, `did_you_know`, `made_worse_by`, `how_its_diagnosed`,"
						sql_con3 = "`questions_to_ask_your_dr`, `treatment`, `self_care`, `risk_factors`, `when_to_see_a_doctor`, `fact`) VALUES ("
						sql_con4 = '"'+item_con['name']+'",'+'"'+item_con['id']+'",'+'"'+str(symp_list)+'",'+'"'+condition_description +'",'
						sql_con5 = '"'+what_to_expect+'",'+'"'+how_common+'",'+'"'+did_you_know+'",'+'"'+made_worse_by+'",'+'"'+how_its_diagnosed+'",'
						sql_con6 = '"'+questions_to_ask_your_dr+'",'+'"'+treatment+'",'+'"'+self_care+'",'+'"'+risk_factors+'",'
						sql_con7 = '"'+when_to_see_a_doctor+'",'+'"'+fact+'"'+')'
						sql_con = sql_con1 + sql_con2+sql_con3+sql_con4+sql_con5+sql_con6+sql_con7 
						# print sql_con
						cursor.execute(sql_con)
						db.commit()
						print '@@@@@'

					sql1 = "INSERT INTO `Total_info2`( `Age`, `Sex`, `Part_ID`, `Symptom_ID`, `Condition_ID`) VALUES ("
					sql2 = '"'+str(item_age)+'",'+'"'+item_sex+'",'+'"'+str(x)+'",'+'"'+item_sym['id']+'",'+'"'+item_con['id']+'"'+')'
					sql_totalinfo = sql1 + sql2
					# print sql_totalinfo
					cursor.execute(sql_totalinfo)
					db.commit()
					print '######'
					# print item['id']