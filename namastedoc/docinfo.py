#this script is for getting the doc info from namastedoc without reviews 

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

db = MySQLdb.connect("localhost","root","8520","NamasteDoc")
cursor = db.cursor()

remtag = re.compile(r'[<>]')
remslbr = re.compile(r'[()/\.,]')
back_rem = re.compile(r'\\')
flagspec = 0
flag_city = 0
flag_num = 0
def fn (url):
	req = urllib2.Request(url)
	html_page = urllib2.urlopen(req)#.read()
	soup = BeautifulSoup(html_page)
	finalurl = html_page.geturl()
	# return [soup,finalurl]
	return soup

city_li = open('city.txt', 'r').readlines()
specs_li = open('specs.txt', 'r').readlines()
for city in city_li[1:]:
	count = 0
	city = city.lower().rstrip()
	print city
	if city == 'sonipat':
		print 'found city'
		flag_city = 1
	elif flag_city ==0:
		continue

	
	for specs in specs_li:
		specs = specs.rstrip()
		specs = remslbr.sub('',specs)
		specs = '-'.join(specs.lower().split())
		if specs == 'pedodontist':
			flagspec = 1
		elif flagspec == 0:
			continue
		flag_err404 = 0
		for num in range(1,200):
			if num == 2:
				flag_num = 1
			elif flag_num ==0:
				continue

			url = 'http://www.namastedoc.com/%s/%s/?page=%s'%(specs,city,str(num))
			
			while True:
				try:
					print url
					soup1 = fn(url)
					
				except urllib2.HTTPError,err:
					if err.code == 404 or  err.code==401 or err.code ==500:
						print '404 pg nt fnd'
						flag_err404 = 1
						break
					else:
						print 'line 140'
						continue
				except:
					print "line 115 err" ,url
					print 'loop untils err is solved :)'
					continue
				else:
					break

			if flag_err404 == 1:
				flag_err404 = 0
				break

			print 'line 60'
			# soup1 = BeautifulSoup (open('srcpg.html'))
			div_container = soup1.find('div',{'class':'container-pad'})
			doc_row = div_container.find_all('div',{'class':'span5 doc-info'})
			print 'line 63'
			if not doc_row:
				print 'empty'
				break
			for item_docrow in doc_row:
				# print item_docrow
				href = 'http://www.namastedoc.com'+item_docrow.a['href']
				href = href.encode('ascii','ignore')
				print href
				print '####'

				###cheks if url is present or not
				sqlupdate = "SELECT `specs_script` FROM `doc_info2` WHERE `Doc_URL`="+'"'+href+'"'
				# print sqlupdate
				a=cursor.execute(sqlupdate)
				# print a
				
				if not a :
					
					print "not there"
				else:
					# doc_dict_json[href].append(type_doc)
					res= cursor.fetchone ()
					res = back_rem.sub('',str(res)) + str(specs)+'$$'
					
					res = MySQLdb.escape_string(str(res))
					# print res
					sqlupdate = "update `doc_info2` set `specs_script`="+'"'+str(res)+'"'+" where `Doc_URL` ="+'"'+href+'"'
					# print sqlupdate
					cursor.execute(sqlupdate)
					db.commit()
					print 'updated::',href
					continue

				# soup = BeautifulSoup (open('srcpg.html'))
				flag_err4041 = 0
				while True:
					try:
						soup = fn(href)
						
					except urllib2.HTTPError,err:
						if err.code == 404 or  err.code==401 or err.code ==500:
							print '404 pg nt fnd'
							flag_err4041 = 1
							break
						else:
							print 'line 140'
							continue
					except:
						print "line 115 err" ,url
						print 'loop untils err is solved :)'
						continue
					else:
						break

				if flag_err4041 == 1:
					flag_err4041 = 0
					break
				
				doc_info = {'Awards/Membership':'NF','Hospital Affiliations':'NF','Specialties':'NF','Education':'NF','Experience':'NF'}
				main_container = soup.find('div',{'class':'container main'})

				row1 = main_container.find('div',{'class':'row-fluid'})
				div_span6 = row1.find('div',{'class':'span6'})
				##using regex to get name
				try:
					name = re.search(r'>.*?<',str(div_span6.h3))
					name =name.group()
					name = remtag.sub('',name)
					doc_info.update({'name':name})
				except:
					print 'url not found'
					continue

				###brief Qualification
				brief_Quali = div_span6.h3.span.text.encode('ascii','ignore')
				doc_info.update({'brief_Quali':brief_Quali})


				row2 = main_container.find('div',{'class':'bs-docs-example'})
				###find container containing tab
				tab_container = row2.find('div',{'class':'tab-content-outer'})

				####doc prof details
				doc_prof = tab_container.find('div',{'id':'doctor_profile'})
				ul_tags = doc_prof.find_all('ul')
				# print (ul_tags[0].previous_sibling.previous_sibling)

				for item_ul in ul_tags:
					list_li = []
					heading = item_ul.previous_sibling.previous_sibling
					heading = ' '.join(heading.text.encode('ascii','ignore').split())
					for list_item in item_ul.find_all('li'):
						list_li.append(' '.join(list_item.text.encode('ascii','ignore').split()))

					doc_info.update({heading:list_li})
				# print (doc_info)

				###doc clinic details
				book_apptab = tab_container.find('div',{'id':'book_an_appointment'})
				hospi_info = book_apptab.find_all('div',{'class':'hospital-info'})
				clinics_info = []
				for item_hospi in hospi_info:
					clinic_list = []
					###clinic name
					heading = item_hospi.find('div',{'class':'heading'})
					heading = ' '.join(heading.text.encode('ascii','ignore').split())
					clinic_list.append('name:'+str(heading))
					###address
					address = item_hospi.find('span',{'class':'address'})
					address = ' '.join(address.text.encode('ascii','ignore').split())
					clinic_list.append('address:'+str(address))
					###fees
					try:
						fees = item_hospi.find('span',{'class':'fees'})
						fees = ' '.join(fees.text.encode('ascii','ignore').split())
						clinic_list.append(str(fees))
					except:
						clinic_list.append('fees:'+'NF')

					###all clinic info in alist
					clinics_info.append(clinic_list)

				doc_info["Specialties"] = MySQLdb.escape_string((str(doc_info["Specialties"])))
				doc_info["Awards/Membership"] = MySQLdb.escape_string((str(doc_info["Awards/Membership"])))
				doc_info["Hospital Affiliations"] = MySQLdb.escape_string((str(doc_info["Hospital Affiliations"])))
				# doc_info["membership"] = MySQLdb.escape_string((str(doc_info["membership"])))					
				doc_info["Education"] = MySQLdb.escape_string((str(doc_info["Education"])))
				doc_info["Experience"] = MySQLdb.escape_string((str(doc_info["Experience"])))
				clinics_info = MySQLdb.escape_string((str(clinics_info)))
												

				sql1 = 'INSERT INTO `doc_info2`( `Name`, `Educ_brief`, `Specialities`, `Awards/Membership`,'
				sql2 = '`Hospital Affiliations`, `Education`, `Experience`, `Clinic_Infos`, `specs_script`, `city`, `Doc_URL`) VALUES ('
				sql3 = '"'+doc_info['name']+'",'+'"'+doc_info['brief_Quali']+'",'+'"'+doc_info['Specialties']+'",'+'"'+doc_info['Awards/Membership']+'",'
				sql4 = '"'+doc_info['Hospital Affiliations']+'",'+'"'+doc_info['Education']+'",'+'"'+doc_info['Experience']+'",'+'"'+str(clinics_info)+'",'
				sql5 = '"'+specs+'",'+'"'+city+'",'+'"'+href+'"'+')'
				sql = sql1+sql2+sql3+sql4+sql5
				# print sql
				cursor.execute(sql)
				db.commit()
				# print sql
				# print clinics_info
				print '$$$$$$$$$$$$$'
