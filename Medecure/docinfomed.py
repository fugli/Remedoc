
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

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket

db = MySQLdb.connect("localhost","root","8520","Medecure")
cursor = db.cursor()

remtag = re.compile(r'[<>]')
remslbr = re.compile(r'[()/\.]')
back_rem = re.compile(r'[\\()\'\"]')
srch = re.compile(r'Fee')

def fn (url):
	req = urllib2.Request(url)
	html_page = urllib2.urlopen(req)#.read()
	soup = BeautifulSoup(html_page)
	finalurl = html_page.geturl()
	# return [soup,finalurl]
	return soup

flagspec = 0
flag_city = 0
city_li = open('city.txt', 'r').readlines()
specs_li = open('speciality.txt', 'r').readlines()
for city in city_li:
	
	city = city.lower().rstrip()
	print city
	if city == 'panjim':
		print 'found city'
		flag_city = 1
	elif flag_city ==0:
		continue

	
	for specs in specs_li:
		specs = specs.rstrip()
		specs = remslbr.sub('',specs)
		specs = '-'.join(specs.lower().split())
		if specs == 'gastroenterology':
			flagspec = 1
		elif flagspec == 0:
			continue
		flag_err404 = 0
		for num in range(1,20):
			# if num == 1:
			# 	flag_num = 1
			# elif flag_num ==0:
			# 	continue


			doc_info = {'Qualification':'NF','Practicing Since':'NF','Speciality':'NF','Conditions Treated':'NF','Language Spoken':'NF','Area of Practice':'NF'}
			url = 'http://www.medecure.com/keyword/doctors/%s/%s/all/by-popularity/page-%s.html'%(specs,city,str(num))
			# soup1 = BeautifulSoup (open('srcpg.html'))

			while True:
				try:
					print url
					soup3 = fn(url)
					
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

			
			doc_div = soup3.find('div',{'id':'doctordiv'})
			doc_list = doc_div.find_all('div',{'class':'left listing_maindiv'})

			for item_docli in doc_list:
				doc_link = item_docli.find('div',{'class':'listing_new_info_div left'})
				doc_link = doc_link.find('div',{'class':'left name_div'})
				doc_link = doc_link.a['href']
				# print doc_link
				timing_div = item_docli.find('div',{'class':'listing_info_new_right right'})
				timing = (timing_div.find_all('div',{'class':'left'}))
				timing = timing[-1]#.text.encode('ascii','ignore')
				# if re.search(r'Fee',timing):
				# 	print 'timing'
				# else:
				try:
					a = re.search(r'<b>.*<br/>',str(timing))
					timing = a.group()
					doc_info.update({'timing':timing})
					

				except:
					doc_info.update({'timing':'NF'})
					

				
				

				###cheks if url is present or not
				sqlupdate = "SELECT `specs_script` FROM `doc_info` WHERE `Doc_URL`="+'"'+doc_link+'"'
				# print sqlupdate
				a=cursor.execute(sqlupdate)
				# print a
				
				if not a :
					
					print "not there",doc_link
				else:
					# doc_dict_json[href].append(type_doc)
					res= cursor.fetchone ()
					if not re.search(str(specs),str(res)):
						print 'spec not present'
						res = back_rem.sub('',str(res)) + str(specs)+'$$'
						
						res = MySQLdb.escape_string(str(res))
						# print res
						sqlupdate = "update `doc_info` set `specs_script`="+'"'+str(res)+'"'+" where `Doc_URL` ="+'"'+doc_link+'"'
						# print sqlupdate
						cursor.execute(sqlupdate)
						db.commit()
					print 'updated::',doc_link
					continue


				soup1 = fn(doc_link)

				div_docname = soup1.find('div',{'class':'doctor_name-details left'})
				##name
				name = div_docname.find('div',{'class':'big_font dark_blue open_sans left profile_blue tips '})
				name = ' '.join(name.text.encode('ascii','ignore').split())
				doc_info.update({'name':name})

				###speclty
				specialty = div_docname.find('div',{'class':'specialist_in open_sans left'})
				specialty = ' '.join(specialty.text.encode('ascii','ignore').split())
				doc_info.update({'specialty':specialty})

				###prof details
				div_profdet = soup1.find('div',{'class':'doctor_profile-details-leftdiv left'})
				###image
				img_link = div_profdet.find('div',{'class':'profile_img left'})
				img_link = img_link.img['src']
				doc_info.update({'img_link':img_link})

				###other detail
				div_oth = div_profdet.find('div',{'class':'profile_info right'})
				table_row = div_oth.find_all('tr')

				for item_tr in table_row[1:]:
					item_td = item_tr.find_all('td')
					item_td[0] = item_td[0].text.encode('ascii','ignore')
					item_td[2] = item_td[2].text.encode('ascii','ignore')
					doc_info.update({item_td[0]:item_td[2]})

				div_profdet_ri8 = soup1.find('div',{'class':'doctor_profile-details-rightdiv right'})
				div_rating = div_profdet_ri8.find('div',{'class':'ratings'})
				rating = len(div_rating.find_all('div',{'class':'ratings_vote'}))
				doc_info.update({'rating':str(rating)})

				###clinic Details

				clnics_div = soup1.find_all('div',{'class':'profile_details_bar left open_sans'})
				clinic_infoli = []
				for item in clnics_div:
					clinic_info = []
					clinic_link = (item.find('a'))
					clinic_link = clinic_link['href']
					clinic_link = clinic_link.encode('ascii','ignore')
					###clinic_link
					clinic_info.append('clinic_link:'+clinic_link)
					print clinic_link
					
					soup2 = fn(clinic_link)
					
						
					main_div = soup2.find('div',{'class':'maindiv'})
					###clinica name
					try:
						clinic_name = main_div.find('div',{'class':'big_font dark_blue  left profile_blue'})
						clinic_name = ' '.join(clinic_name.text.encode('ascii','ignore').split())
						clinic_info.append('name:'+clinic_name)
					except:
						print 'clinic NF'
						continue
					###clinic_image
					clinic_img_div = main_div.find('div',{'class':'hospital_imgmaindiv left'})
					clinic_img = clinic_img_div.find('div',{'class':'profile-clinic-img left'})
					clnic_img = clinic_img.img['src']
					clinic_info.append('img:'+clnic_img)
					###rating
					div_rating = main_div.find('div',{'class':'ratings'})
					rating = 5 - len(div_rating.find_all('div',{'class':'ratings_blank'}))
					clinic_info.append('rating:'+str(rating))
					###hosp detail
					hosp_det_div = main_div.find('div',{'class':'hospital_details_left'})
					for item_tr in hosp_det_div.find_all('tr'):
						item_td = item_tr.find_all('td')
						item_td[0] = item_td[0].text.encode('ascii','ignore')
						tag_item = item_td[2]
						item_td[2] = item_td[2].text.encode('ascii','ignore')
						item_td[2] = re.sub(r'(View map)','',item_td[2])
						###maplink
						if item_td[0] == 'Address':
							try:
								map_link = tag_item.find('div',{'class':'left margin-top5'})
								map_link = map_link.a['rel']
							except:
								map_link = "NF"
							# print map_link
							clinic_info.append('map_link:'+str(map_link))
						clinic_info.append(item_td[0] + ':'+item_td[2])
					clinic_infoli.append(clinic_info)
				# print clinic_infoli
				###about award
				div_proftab = soup1.find_all('div',{'class':'profile_tab'})


				# print doc_info

				doc_info["specialty"] = MySQLdb.escape_string((str(doc_info["specialty"])))
				doc_info["Speciality"] = MySQLdb.escape_string((str(doc_info["Speciality"])))
				doc_info["Language Spoken"] = MySQLdb.escape_string((str(doc_info["Language Spoken"])))
				doc_info["Qualification"] = MySQLdb.escape_string((str(doc_info["Qualification"])))					
				doc_info["Practicing Since"] = MySQLdb.escape_string((str(doc_info["Practicing Since"])))
				doc_info["Area of Practice"] = MySQLdb.escape_string((str(doc_info["Area of Practice"])))
				clinic_infoli = MySQLdb.escape_string((str(clinic_infoli)))
				doc_info["timing"] = MySQLdb.escape_string((str(doc_info["timing"])))


				sql1 = 'INSERT INTO `doc_info`(`Name`, `Speciality_nr_name`, `Speciality_all`, `Lang`, `Quali`,'
				sql2 = ' `Conditions Treated`, `Practicing Since`, `Area of Practice`, `clinic_info`, `specs_script`,'
				sql3 = ' `Doc_URL`, `City`,`doc_rating`, `timing`, `Doc_imgsrc`) VALUES ('
				sql4 = '"'+doc_info['name']+'",'+'"'+doc_info['specialty']+'",'+'"'+doc_info['Speciality']+'",'+'"'+doc_info['Language Spoken']+'",'
				sql5 = '"'+doc_info['Qualification']+'",'+'"'+doc_info['Conditions Treated']+'",'+'"'+doc_info['Practicing Since']+'",'+'"'+doc_info['Area of Practice']+'",'
				sql6 = '"'+(clinic_infoli)+'",'+'"'+specs+'",'+'"'+doc_link+'",'+'"'+city+'",'+'"'+doc_info['rating']+'",'+'"'+doc_info['timing']+'",'+'"'+doc_info['img_link']+'"'+')'
				sql = sql1+sql2+sql3+sql4+sql5+sql6
				# print sql
				cursor.execute(sql)
				db.commit()
				print '#######################'