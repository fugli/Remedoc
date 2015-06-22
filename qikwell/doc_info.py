from bs4 import BeautifulSoup
import re
import urllib2
import MySQLdb
import string
import requests

# import socks
# import socket
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
# socket.socket = socks.socksocket


db = MySQLdb.connect("localhost","root","8520","Qikwell")
cursor = db.cursor()

back_rem = re.compile(r'\\')

def fn (url):
	html_page = urllib2.urlopen(url)
	soup = BeautifulSoup(html_page)
	return soup
flagspec = 0
flag = 0
flag_city = 0
flag_num = 0
flag_err = 0
# print>>open('clinic_lnk.txt','w'),''
city_li = open('city.txt', 'r').readlines()
specs_li = open('spec_qikwell.txt', 'r').readlines()
for city in city_li:
	count = 0
	city = city.rstrip()
	print city
	if city == 'Vijayawada':
		print 'found city'
		flag_city = 1
	elif flag_city ==0:
		continue

	
	# for specs in specs_li:
	# 	specs = specs.rstrip()
	# 	specs = '-'.join(specs.split())
	# 	if specs == 'Ophthalmologist':
	# 		flagspec = 1
	# 	elif flagspec == 0:
	# 		continue
	specs = 'NULL'
	for num in range(1,200):
		if num == 1:
			flag_num = 1
		elif flag_num ==0:
			continue
		# url = 'http://www.qikwell.com/doctors/%s/'%str(city)+str(specs)+'?page='+str(num)
		url = 'http://www.qikwell.com/doctors/%s/'%str(city)+'?page='+str(num)
		# url = 'http://www.qikwell.com/doctors/Bangalore/Dentist?page=7'
		# soup = BeautifulSoup (open('srcpg.html'))
		

		while True:
			try:
				print url
				soup = fn(url)
			except urllib2.HTTPError as err:
				if err.code == 410 or err.code==404:
					print 'err 410'
					flag_err = 1
					break
				else:
					print err.code , 'loops '
					continue
			except:
				print 'loop until err solveed'
				continue
			else:
				break
		if flag_err ==1:
			continue

		flag_err = 0
		print '28'
		div_doc_list = soup.find('div',{'class':'doctors-list'})
		try:
			div_docs = div_doc_list.find_all('div',{'itemtype':'http://schema.org/Physician'})
		except:
			print 'No doc '
			break
		if not div_docs:
			print 'empty'
			break

		for item_div_docs in div_docs:
			doc_info = {}
			count = count +1 

			profile1 = item_div_docs.find('div',{'class':'profile clearfix col-lg-7 col-md-7 col-sm-7 col-xs-12'})
			###doc image
			imgsrc = (profile1.find('div',{'class':'img-holder'})).img['src']
			doc_info.update({'imgsrc':imgsrc})

			###doc exp name
			prof_right = profile1.find('div',{'class':'right'})
			try:
			###exp
				exp = prof_right.find('div',{'class':'experience hide'}).text.encode('utf-8')
				doc_info.update({'exp':exp})
			except:
				pass
			
			####doc_link
			atag = profile1.find('a',{'class':'name'})
			doc_link = atag['href']
			doc_link = 'http://www.qikwell.com'+str(doc_link)
			doc_info.update({'doc_link':doc_link})

			sqlu = 'select spec_script from doc_info where doc_url = '+'"'+doc_link+'"'
			a = cursor.execute(sqlu)
			
			if a:
				res= cursor.fetchone ()
				# res = back_rem.sub('',str(res)) + str(specs)+'$$'
				
				# res = MySQLdb.escape_string(str(res))
				# print res
				# sqlupdate = "update `doc_info` set `spec_script`="+'"'+str(res)+'"'+" where `doc_url` ="+'"'+doc_link+'"'
				# # print sqlupdate
				# cursor.execute(sqlupdate)
				# db.commit()

				print "updated::::" ,doc_link
			else:
				flag = 1

			if flag == 0:
				continue
			flag = 0
			##name
			try:	
				name = ' '.join(atag.text.encode('utf-8').split())
				doc_info.update({'name':name})
			except:
				doc_info.update({'name':'NF'})
				pass

			####qualification
			div_info = prof_right.find('div',{'class':'info'})
			qualification = div_info.find('div',{'class':'qualification'}).text.encode('ascii','ignore')
			qualification = ' '.join(qualification.split())
			doc_info.update({'qualification':qualification})
			####speiality and about
			spec_clinic = div_info.find_all('div',{'class':''}) 
			speciality = ' '.join(spec_clinic[0].text.split())
			about = ' '.join(spec_clinic[2].text.encode('ascii','ignore').split())#.encode('utf-8').split())
			doc_info.update({'speciality':speciality})
			doc_info.update({'about':about})
			
			# try:
			# 	clinic_info = []
			# 	for atags in (spec_clinic[1]).find_all('a'):
			# 		print atags
			# 		clinic_link = 'http://www.qikwell.com/clinics/'+atags['href']
			# 		clinic_afflia = atags.find('span',{'itemprop':'hospitalAffiliation'}).text.encode('utf-8')
			# 		clinic_add = atags.find('span',{'itemprop':'addressLocality'}).text.encode('utf-8')
			# 		clinic_info.append(str(' '.join(clinic_add.split())) + '$$')
			# 		clinic_info.append(str(' '.join(clinic_afflia.split())) + '$$')
			# 		clinic_info.append(clinic_link)

			# 		doc_info.update({'clinic_info':clinic_info})

				
			# except:
			# 	pass
			# print clinic_link
			# print clinic_afflia


			profile2 = item_div_docs.find('div',{'class':"about col-lg-5 col-md-5 col-sm-5 col-xs-12"})
			####languages
			try:
				div_lang = profile2.find('div',{'class':'line clearfix lang'})
				lang = div_lang.find('span',{'class':'text right'}).text
				lang = ' '.join(lang.split())#.encode('utf-8').split())
				doc_info.update({'lang':lang})
			except:
				doc_info.update({'lang':'NF'})
			try:
				fees = profile2.find('div',{'class':'left ttip'}).text
				fees = ' '.join(fees.encode('utf-8').split())
				doc_info.update({'fees':fees})
			except:
				doc_info.update({'fees':'NF'})
				pass
			####recomendation
			try:
				i_tag = profile2.find('i',{'class':'qicon-super'})
				recomend = (i_tag).parent.text.encode('utf-8')
				doc_info.update({'recomend':recomend})
			except:
				doc_info.update({'recomend':'NF'})
				
				pass
			# print lang
			# print len(div_clearfix)
			# print (spec_clinic)

			# print doc_info
			print doc_link

			soup2 = fn(doc_link)
			####getting clinic info
			sec2 = soup2.find('section',{'class':'two-column statement-location'})
			div_loc = sec2.find('div',{'class':'location col col-sm-6 col-xs-12'})
			div_cl_li = div_loc.find('div',{'class':'clinics-list'})
			clinic_info_list = []
			for item_li in div_cl_li.find_all('div',{'class':'clinic'}):
				clinic_info = []
				div_name = item_li.find('div',{'class':'name'})
				clinic_link = div_name.a['href']
				clinic_file = open('clinic_lnk.txt','r').readlines()
				if not clinic_link+'\n' in clinic_file:
					print>>open('clinic_lnk.txt','a'),clinic_link
				name = div_name.text.encode('utf-8')
				clinic_info.append(name)
				clinic_info.append(clinic_link)
				div_add = item_li.find('div',{'class':'address'})
				street_add = div_add.find('span',{'itemprop':'streetAddress'}).text#.encode('utf-8')
				add_loclty =  div_add.find('span',{'itemprop':'addressLocality'}).text#.encode('utf-8')
				ad_region = div_add.find('span',{'itemprop':'addressRegion'}).text#.encode('utf-8')
				pin_code =  div_add.find('span',{'itemprop':'postalCode'}).text#.encode('utf-8')
				clinic_info.extend(['street:'+street_add,'locality:'+str(add_loclty) ,'region:'+str(ad_region), 'pin:'+pin_code])
				clinic_info_list.append(clinic_info) 

			# print clinic_info_list

			####teatment offered
			sec3 = soup2.find('section',{'class':'two-column treatment-affliation'})
			# print sec3
			# print sec3
			try:
				treatment = sec3.find('div',{'class':'treatment col first col-sm-6 col-xs-12'})
				treat_offerd = []
				tr_li = treatment.find_all('li')
				# print tr_li
				for item_li in tr_li:
					item = item_li.text.encode('utf-8')
					treat_offerd.append(item)
				# print treat_offerd
				doc_info.update({'treat_offerd':treat_offerd})
			except:
				doc_info.update({'treat_offerd':'NF'})
				pass

			####affiation
			try:
				affilia_offerd = []
				affiliation = sec3.find('div',{'class':'affiliation col last col-xs-12 col-sm-6'})
				af_li = affiliation.find_all('li')
				for item_li in af_li :
					item = item_li.text.encode('utf-8')
					affilia_offerd.append(item)
				# print affilia_offerd
				doc_info.update({'affilia_offerd':affilia_offerd})
			except:
				doc_info.update({'affilia_offerd':'NF'})
				pass
			# print doc_info
			doc_info["affilia_offerd"] = MySQLdb.escape_string(str(doc_info["affilia_offerd"]))
			doc_info["treat_offerd"] = MySQLdb.escape_string(str(doc_info["treat_offerd"]))
			clinic_info_list =  MySQLdb.escape_string(str(clinic_info_list))
			doc_info["qualification"] =  MySQLdb.escape_string(str(doc_info["qualification"]))
			doc_info["name"] = MySQLdb.escape_string(str(doc_info["name"]))
			doc_info["speciality"] = MySQLdb.escape_string(str(doc_info["speciality"]))
			doc_info["lang"] = MySQLdb.escape_string(str(doc_info["lang"]))
			doc_info["about"] = MySQLdb.escape_string(str(doc_info["about"]))
			# print doc_info['lang'],doc_info['qualification'],doc_info['about'],str(clinic_info_list)

			sql1 = 'INSERT INTO `doc_info`(`Name`, `Speciality`, `Recommendation`, `Fees`, `Lang`, `Qualification`,'
			sql2 = '`About`, `Clinic_Infos`, `Doc_imgsrc`, `treatment_offered`, `past_affiliation`, `doc_url`, `spec_script`,`City`) VALUES ('
			sql3 = '"'+doc_info['name']+'",'+'"'+doc_info['speciality']+'",'+'"'+doc_info['recomend']+'",'+'"'+doc_info['fees']+'",'
			sql4 = '"'+doc_info['lang']+'",'+'"'+doc_info['qualification']+'",'+'"'+doc_info['about']+'",'+'"'+str(clinic_info_list)+'",'+'"'+doc_info['imgsrc']+'",'
			sql5 = '"'+doc_info['treat_offerd']+'",'+'"'+doc_info['affilia_offerd']+'",'+'"'+doc_info['doc_link']+'",'+'"'+specs+'",'
			sql6 = '"'+city + '"'+')'

			# sql3 = sql3.encode('ascii', 'ignore')
			sql = sql1 + sql2 + sql3 + sql4 + sql5 + sql6
			# print sql
			# print type(sql)
			cursor.execute(sql)
			db.commit()
			print '###############################'+'\n'

	print count,'$$$$$$$$$$$$$','\n'

