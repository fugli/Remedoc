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

db = MySQLdb.connect("localhost","root","8520","Lyberate")
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
city_li = open('locality.txt', 'r').readlines()
for city in city_li:
	city = city.lower().rstrip()
	# print city
	# if city == 'panjim':
	# 	print 'found city'
	# 	flag_city = 1
	# elif flag_city ==0:
	# 	continue

	flag_err404 = 0
	flag_empty = 1
	for num in range(1,10):

		# if num == 1:
		# 	flag_num = 1
		# elif flag_num ==0:
		# 	continue


		# url = 'https://www.lybrate.com'+city+'?page='+str(num)
		url =city+'?page='+str(num)
		print url
		soup2 = fn(url)

		div_doc_li = soup2.find_all('div',{'class':'name_block'})
		if not div_doc_li :
			flag_empty = 1
			print 'empty'
			break
		for item in div_doc_li:
			# item= item.find('div',{'class':'name_block'})
			doc_link =  item.a['href'].encode('ascii','ignore')
			doc_link = 'https://www.lybrate.com'+str(doc_link)
			# print doc_link

			###cheks if url is present or not
			sqlupdate = "SELECT `city` FROM `doc_info` WHERE `Doc_URL`="+'"'+doc_link+'"'
			# print sqlupdate
			a=cursor.execute(sqlupdate)
			# print a
			
			if not a :
				
				print "not there",doc_link
			else:
				# doc_dict_json[href].append(type_doc)
				res= cursor.fetchone ()
				print res
				if not re.search(str(city),str(res)):
					print 'spec not present'
					res = back_rem.sub('',str(res)) + str(city)+'$$'
					
					res = MySQLdb.escape_string(str(res))
					# print res
					sqlupdate = "update `doc_info` set `city`="+'"'+str(res)+'"'+" where `Doc_URL` ="+'"'+doc_link+'"'
					# print sqlupdate
					cursor.execute(sqlupdate)
					db.commit()
				print 'updated::',doc_link
				continue


			soup1 = fn(doc_link)


			soup1 = BeautifulSoup (open('srcpg.html'))
			doc_link ='bls'
			city = 'bla'
			doc_info = {}
			doc_main = soup1.find('div',{'class':'main_top_block'})
			###left part-- name etc

			div_left = doc_main.find('div',{'class':'span6'})

			##image
			doc_img = div_left.find('img')
			doc_img = doc_img['src']
			doc_info.update({'doc_img':doc_img})

			##name briefspec,recomm,helped
			div_nameblk = div_left.find('div',{'class':'name_block'})
			span_name = div_nameblk.find('span',{'itemprop':'name'})
			name = ' '.join(span_name.h1.text.encode('ascii','ignore').split())
			doc_info.update({'name':name})

			##degree
			div_deg = div_left.find('div',{'class':'degrees'})
			degree = ' '.join(div_deg.text.encode('ascii','ignore').split())
			doc_info.update({'degree':degree})

			##brief spec
			div_bspec = div_left.find('div',{'class':'specialty'})
			bspec = ' '.join(div_bspec.text.encode('ascii','ignore').split())
			doc_info.update({'bspec':bspec})

			##reccom,peop helped
			credit = {'Recommendation':'NF','Helped':'NF'}
			cred_li = div_left.find_all('div',{'class':'cred'})
			for item_cred in cred_li:
				item_cred = ' '.join(item_cred.text.encode('ascii','ignore').split())
				if re.search(r'Recommendation',str(item_cred)):
					credit.update({'Recommendation':item_cred})
				elif re.search(r'Helped',str(item_cred)):
					credit.update({'Helped':item_cred})

			###Doc reco,exp,fee(middle part)
			mid_li = {'Recommendation':'NF','Experience':'NF','Fee':'NF'}
			div_middle = doc_main.find('div',{'class':'span3 middle_block'})
			div_mid_li = div_middle.find_all('div',{'class':'right_margin_icon'})
			for item_mid_li in div_mid_li:
				item_mid_li = ' '.join(item_mid_li.text.encode('ascii','ignore').split())
				# print item_mid_li
				if re.search(r'Recommendation',str(item_mid_li)):
					mid_li.update({'Recommendation':item_mid_li})
				elif re.search(r'Experience',str(item_mid_li)):
					mid_li.update({'Experience':item_mid_li})
				elif re.search(r'Fee',str(item_mid_li)):
					# print 'fee','#######$$$$$$'
					mid_li.update({'Fee':item_mid_li})
			# print name,degree,bspec,mid_li
			###right part##about
			div_abt = doc_main.find('span',{'itemprop':'description'})
			div_abt = div_abt.find('div',{'class':'small_detail'})
			# more_abt = div_abt.find('div')
			# more_abt = ' '.join(more_abt.text.encode('ascii','ignore').split())
			div_abt = ' '.join(div_abt.text.encode('ascii','ignore').split())
			a = re.split('More about %s'%name,str(div_abt))
			prsnl_stmt = a[0]
			more_about = a[1]
			doc_info.update({'more_abt':a[1]})
			doc_info.update({'prsnl_stmt':a[0]})


			# print	(div_all[0])#.next_sibling#.previous_sibling#div_abt # div_abt#about
			# print div_abt
			# a= re.search(r'(>.*?<)',str(div_abt))
			# print a.group()

			###profile details
			prof_det = soup1.find('div',{'class':'profile_details'})
			div_span4 = prof_det.find('div',{'class':'span4'})
			###photos
			try:
				div_photos = div_span4.find('div',{'class':'photos heading'})
				photos_li = []
				for item_photos in div_photos.find_all('div',{'class':'item'}):
					photos_li.append(item_photos.a['href'])
				doc_info.update({'photos_li':photos_li})
			except :
				print 'photos NF'
				doc_info.update({'photos_li':"NF"})


			###speciality
			speciality = []
			try:
				div_specs = div_span4.find('div',{'class':'user_sub_speciality heading'})
				div_specs_li = div_specs.find_all('div',{'class':'item'})
				for item_speci in div_specs_li:
					item_speci = ' '.join(item_speci.text.encode('ascii','ignore').split())
					speciality.append(item_speci)
				doc_info.update({'speciality':speciality})
			except :
				print 'specs NF'
				doc_info.update({'speciality':"NF"})

			###education
			educ_li = []
			try:
				div_educ = div_span4.find('div',{'class':'education heading'})
				for item_speci in div_educ.find_all('div',{'class':'items'}):
					educ = []
					for item in item_speci.find_all('div',{'class':'item'}):
						item = ' '.join(item.text.encode('ascii','ignore').split())
						educ.append(item)
					educ_li.append(educ)
				doc_info.update({'educ_li':educ_li})
			except :
				print 'edu NF'
				doc_info.update({'educ_li':"NF"})

			# print educ_li



			div_span = prof_det.find('div',{'class':'span8'})
			clinic_blk = prof_det.find('div',{'class':'block'})

			###clinic info
			clinic_info = []
			span = clinic_blk.find('span',{'class':'clinics'})
			name_blk = span.find('div',{'class':'name_block'})
			##name
			div_name = name_blk.find('div',{'class':'name'})
			name = ' '.join(div_name.text.encode('ascii','ignore').split())
			clinic_info.append('name::'+name)
			###link
			clinic_link = div_name.a['href']
			clinic_info.append('link::'+clinic_link)
			print name,clinic_link
			###time
			time_li = []
			div_time_li = name_blk.find_all('time')
			for item_time in div_time_li:
				item_time = ' '.join(item_time.text.encode('ascii','ignore').split())
				# print item_time
				time_li.append(item_time)
			# print time_li
			###address
			address = []
			div_add = name_blk.find('div',{'itemprop':'address'})
			###street add
			span_st_add = div_add.find('span',{'itemprop':'streetAddress'})
			span_st_add = ' '.join(span_st_add.text.encode('ascii','ignore').split())
			address.append('street_add::'+str(span_st_add))
			###locality
			# try:
			span_loc_add = div_add.find('span',{'itemprop':'addressLocality'})
			span_loc_add = ' '.join(span_loc_add.text.encode('ascii','ignore').split())
			address.append('locality::'+str(span_loc_add))
			# except:
			# 	raise
			###pincode
			span_pin_add = div_add.find('span',{'itemprop':'postalCode'})
			span_pin_add = ' '.join(span_pin_add.text.encode('ascii','ignore').split())
			address.append('postalCode::'+str(span_pin_add))

			clinic_info.append('address::'+str(address))

			###clinic location
			div_loc = clinic_blk.find('div',{'class':'right-btn action-btns'})
			loc_link = div_loc.a['href']
			clinic_info.append('loc_link::'+str(loc_link))
			# print clinic_info
			# print doc_info
			# print credit
			# print mid_li
				# except:
				# 	print 'NF'
				# 	continue

			doc_info["educ_li"] = MySQLdb.escape_string((str(doc_info["educ_li"])))
			doc_info["speciality"] = MySQLdb.escape_string((str(doc_info["speciality"])))
			doc_info["degree"] = MySQLdb.escape_string((str(doc_info["degree"])))
			doc_info["more_abt"] = MySQLdb.escape_string((str(doc_info["more_abt"])))					
			# doc_info["Practicing Since"] = MySQLdb.escape_string((str(doc_info["Practicing Since"])))
			# doc_info["Area of Practice"] = MySQLdb.escape_string((str(doc_info["Area of Practice"])))
			clinic_info = MySQLdb.escape_string((str(clinic_info)))
			# doc_info["timing"] = MySQLdb.escape_string((str(doc_info["timing"])))

			sql1 = 'INSERT INTO `doc_info`(`Name`, `Doc_URL`, `Education`, `Speciality`, `doc_img`, `Degree`,`More_About`,'
			sql2 = '`brief_spec`, `Recommendation`, `Helped`, `Fee`, `Doc_Reccomendation`, `clinic_info`, `city`,`Experience`, `Gallery`, `Personal_statement`) VALUES ('
			sql4 = '"'+doc_info['name']+'",'+'"'+doc_link+'",'+'"'+doc_info['educ_li']+'",'+'"'+doc_info['speciality']+'",'
			sql5 = '"'+doc_info['doc_img']+'",'+'"'+doc_info['degree']+'",'+'"'+doc_info['more_abt']+'",'+'"'+doc_info['bspec']+'",'
			sql6 = '"'+credit['Recommendation']+'",'+'"'+credit['Helped']+'",'+'"'+mid_li['Fee']+'",'+'"'+mid_li['Recommendation']+'",'
			sql3 = '"'+clinic_info+'",'+'"'+city+'",'+'"'+mid_li['Experience']+'",'+'"'+str(photos_li)+'",'+'"'+doc_info['prsnl_stmt']+'"'+')'
			sql = sql1+sql2+sql4+sql5+sql6+sql3
			# print sql
			cursor.execute(sql)
			db.commit()
			print '#######################'
			