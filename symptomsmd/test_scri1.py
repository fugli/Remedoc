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

def fn (url):
    req = urllib2.Request(url, headers=hdr)
    html_page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html_page)
    return soup

s = requests.Session()
s.headers.update(hdr)
# s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
# r = s.get("http://symptoms.webmd.com/#introView")

# url = 'http://symptoms.webmd.com/'
url_con = 'http://symptoms.webmd.com/scapp/SymptomCheckerAPI.svc/conditions'
url_sym = 'http://symptoms.webmd.com/scapp/SymptomCheckerAPI.svc/symptoms'

sym_id_list = []
print >> open('symptom.txt','w'),''
age = [1,4,8,14,20,30,40,50,60,64]
sex = ['M','F']
for item_sex in sex:
  print item_sex
  for item_age in age:
    print item_age,'#######'
    for x in range(1,65):
#       print x
        body_sym = json.dumps({"request":{"user":{"age":item_age,"gender":item_sex,"zip":"","vid":"1eea18c3-46e3-4c6b-a54f-1aa3ff800e1f"},"locale":"us","bodypartid":x}})
        body_con = json.dumps({"request":{"user":{"age":1,"gender":"M","zip":"","vid":"1eea18c3-46e3-4c6b-a54f-1aa3ff800e1f"},"locale":"us","maxconditions":200,"bodyparts":[{"id":2,"symptoms":[{"id":473,"qclss":[]}]}]}})

        # print body
        r_sym = s.post(url=url_sym, data=body_sym)
        r_con = s.post(url=url_con, data=body_con)
        # print(r.text)
        # print r.request.headers
        print '$$$$$$$$'
        # print dir(r)
        # print r.text.encode('utf-8')
        # out = open('data.txt', 'wt')
        # print json.dump(r.json()['data']['symptoms'], out)
        # print >>open('output.txt','w'), r.content


        for item in r.json()['data']['conditions']:
          if not item['id'] in sym_id_list:
            sym_id_list.append(item['id'])
            print >> open('symptom.txt','a'),item['name'],item['id']
            # print sql
            item['name'] = str(item['name']).encode('utf-8')
            item['id'] = str(item['id']).encode('utf-8')

          # sql = "INSERT INTO `symptoms`( `Symp_Name`, `Symp_ID`) VALUES (" + '"'+item['name']+'",'+'"'+item['id']+'"'+')'
          # cursor.execute(sql)
          # db.commit()

          # print item['id']