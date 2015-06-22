from bs4 import BeautifulSoup
import re
import urllib2
import MySQLdb
import string
import requests
import json

# import socks
# import socket
# socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
# socket.socket = socks.socksocket

db = MySQLdb.connect("localhost","root","8520","Helping_Doc")
cursor = db.cursor()

def fn (url):
	req = urllib2.Request(url)
	html_page = urllib2.urlopen(req)#.read()
	soup = BeautifulSoup(html_page)
	# finalurl = html_page.geturl()
	return soup

TAG_RE = re.compile(r',*\xc2\xa0')

def remove_xc2(text):
	return TAG_RE.sub('', text)


back_rem = re.compile(r'\\')
flag_pres = 0
flag_err = 0
flag_spec = 0
flag_city =0
city_list = open('city.txt','r').readlines()
spec_file = open('specs_hel_doc.txt','r').readlines()

for item_city in reversed(city_list):
	item_city = item_city.rstrip()
	# locality_list = open('%s locality.txt'%str(item_city),'r').readlines()
	city = item_city
	# doc_dict_json = {}
	# with open('%s doc_dict_json.json'%str(city), 'w') as f:    #####dumping dictionary
	# 	json.dump(doc_dict_json, f)

	item_city = "_".join(item_city.lower().split())
	if item_city == 'raipur':
		flag_city =1
	elif flag_city ==0:
		continue
	# for item_locality in locality_list[1:]:
	# 	item_locality = "_".join(item_locality.lower().split())
	item_locality = 'NULL'
	for spec in spec_file:
		spec = "_".join(spec.lower().split())
		if spec == 'hiv_test_specialist':
			flag_spec =1
		elif flag_spec==0:
			continue
		url = 'https://www.helpingdoc.com/'+spec+'-in-'+item_city#+item_locality+'-'+city
		print url

		soup2 = fn(url)
		atag = soup2.find_all("a",{"class":"titel-01"})
		
		for link in atag:
			doc_link = 'https://www.helpingdoc.com'+link['href']
			# print doc_link

			####unique entry only
			# with open('%s doc_dict_json.json'%str(city)) as f:
			#     doc_dict_json = json.load(f)

			# if not doc_dict_json.has_key(doc_link):
			# 	doc_dict_json.update({doc_link:""})
			# 	doc_dict_json[doc_link] = []
			# 	doc_dict_json[doc_link].append(spec)
			# 	flag_pres = 1
			# 	print "above url not there"


			# else:
			# 	doc_dict_json[doc_link].append(spec)

			# 	sqlupdate = "update `hel_docinfo` set `specs_script`="+'"'+str(doc_dict_json[doc_link])+'"'+" where `Doc_link` ="+'"'+doc_link+'"'
			# 	# print sqlupdate
			# 	cursor.execute(sqlupdate)
			# 	db.commit()

			# 	print "above url type updated"

			# with open('%s doc_dict_json.json'%str(city), 'w') as f:    #####dumping dictionary
			# 	json.dump(doc_dict_json, f)

			####below code checks if the url is present in the table hel_doc_info
			sql = 'select specs_script from hel_doc_info2 where `Doc_link` ='+'"'+doc_link+'"'
			a = cursor.execute(sql)
			if  a :
				res= cursor.fetchone ()
				res = back_rem.sub('',str(res)) + str(spec)+'$$'
				
				res = MySQLdb.escape_string(str(res))
				# print res
				sqlupdate = "update `hel_doc_info2` set `specs_script`="+'"'+str(res)+'"'+" where `Doc_link` ="+'"'+doc_link+'"'
				# print sqlupdate
				cursor.execute(sqlupdate)
				db.commit()

				print "updated::::" ,doc_link
			else:
				flag_pres = 1
				print 'not present',doc_link

			
			if flag_pres ==1 :

				doc_info = {}
				flag_pres = 0 

				while True:
					try:
						soup1 = fn(doc_link)
					except urllib2.HTTPError as err:
						if err.code == 410 or err.code==404:
							print 'err 410'
							flag_err = 1
							break
						

						elif err.code == 400:
							print 'err 400'
							print >>open('bad_link.txt','a'),doc_link
							flag_err = 1
							break
						else:
							print err.code , "loops" 
							continue
					except:
						print 'loop until err solveed'
						continue
					else:
						break
				if flag_err ==1:
					flag_err = 0
					continue

				
				
				# soup1 = fn ("https://www.helpingdoc.com/doctor/VKGupta")

				doc_data = soup1.find("div",{"id":"docData"})
				
				####image block ,recommen,prsnal link
				div_img = doc_data.find("div",{"class":" col-lg-3 col-md-3 col-sm-4 col-xs-12  "})
				img_src =( div_img.find("div",{"itemtype":"http://schema.org/VisualArtwork"})).img['src']

				doc_info.update({"img_src":img_src})
				try:
					recomend_by = (div_img.find("div",{"class":"fontForRecomendation col-lg-12 col-md-12 col-sm-12 col-xs-12 auto "})).text.encode('utf-8')
					doc_info.update({"recommen":remove_xc2(recomend_by)})
				except:
					# print "no recommedation"
					doc_info.update({"recommen":"NF"})
				try:
					div_prsnl_link = div_img.find("div",{"class":"col-lg-12 col-md-12 auto hidden-xs"})
					prsnl_link = (div_prsnl_link.find("a"))['href']
					doc_info.update({"prsnl_link":prsnl_link})

				except:
					# print "No link"
					doc_info.update({"prsnl_link":"NF"})
				# print img_src

				####

				div_info = doc_data.find("div",{"class":"col-lg-9 col-md-9 col-sm-8 col-xs-12 auto"})

				div_info_part1 = div_info.find("div",{"class":"one_first"})
				#####doc name
				doc_name = div_info_part1.find("div",{"class":"col-lg-8 col-md-8 col-sm-8 hidden-xs"}).text.encode('utf-8')
				doc_name = " ".join(doc_name.split())
				doc_info.update({"doc_name":doc_name})

				#####doc type
				div_doc_type = div_info_part1.find("div",{"class":"col-lg-4 col-md-4 col-sm-4 col-xs-12 auto"})
				doc_type_list = []
				for item_type in div_doc_type.find_all("div",{"itemprop":"medicalSpecialty"}):
					doc_type_list.append(str(" ".join(item_type.text.encode('utf-8').split())) + "$$")
				doc_info.update({"doc_type_list":doc_type_list})

				##### doc degree

				div_doc_deg = div_info_part1.find("div",{"class":"col-lg-12 col-md-12 hidden-xs "})
				doc_deg_list = []
				for item_deg in div_doc_deg.find_all("li"):
					deg = " ".join(item_deg.text.encode('utf-8').split())
					doc_deg_list.append(remove_xc2(str(deg)+"$$"))
				doc_info.update({"doc_deg_list":doc_deg_list})

				#####doc summary
				div_doc_summ = div_info_part1.find("div",{"class":"col-lg-12 col-md-12 mob-auto"})
				doc_summ = (div_doc_summ.find("p")).text.encode('utf-8')
				doc_summ = remove_xc2(" ".join(doc_summ.split()))
				doc_info.update({"doc_summ":doc_summ})

				#####info part 2
				div_info_part2 = div_info.find_all("div",{"class":"col-md-6 col-lg-6 mob-auto"})
				div_block_lg12 = []
				for item_info2 in div_info_part2:
					for item in item_info2.find_all("div",{"class":"col-lg-12"}):
						div_block_lg12.append(item)

				# print len(div_block_lg12)
				flag = 0
				doc_info.update({"Experience":"NF" , "Languages":"NF" ,"Consultation fee" :"NF" , "Professional Experience":"NF" , "Certifications and Memberships":"NF"})
				doc_info.update({"Qualifications":"NF","Expertise":"NF","Awards and publication":"NF"})
				for item_info in div_block_lg12:
					try:
						h3tag = item_info.find_all("h3",{"class":"title-tag-doctor"})
					except:
						print "errr"
						continue

					for item_h3tag in h3tag:
						title = item_h3tag.text.encode('utf-8')
						title = " ".join(title.split())
						# print title
						
						if title=="Experience" or title=="Languages" or title=="Consultation fee":
							content = item_info.find("div",{"class":"title-tag-inner"}).text.encode('utf-8')
							content = " ".join(content.split())
							doc_info.update({title:remove_xc2(content)})

						elif title == 'Professional Experience' or title == 'Certifications and Memberships': 
							if flag == 0:
							
								content_ul = item_info.find_all("ul",{"class":"line2"})
								count = 0
								
								for item_ul in content_ul:
									count = count +1
									content_list1 = []
									
									for item_content_li in item_ul.find_all("li",{"class":"title-tag-inner"}):
										content = " ".join(item_content_li.text.encode('utf-8').split())
										content_list1.append(remove_xc2(str(content)+"$$"))
									flag =1	
									
									if count==1:			
										doc_info.update({title:content_list1})
									
									if count == 2:
										doc_info.update({'Certifications and Memberships':content_list1})
									# print content_list1
						else:
							
							content_list = []

							content_li = item_info.find_all("li",{"class":"title-tag-inner"})
							for item_content_li in content_li:
								content = " ".join(item_content_li.text.encode('utf-8').split())
								content_list.append(remove_xc2(str(content)+"$$"))

							doc_info.update({title:content_list})

				####clinic and location of doctor
				# div_clinic_add = soup1.find("div",{"class":"col-lg-4 col-md-4 col-sm-12 col-xs-12"})
				# print div_clinic_add
				map_app = soup1.find_all("div",{"class":"map-appointment"})
				clinic_list = []
				for item_map_app in map_app:
					
					try:
						clinic_name = item_map_app.find("div",{"itemtype":"https://schema.org/MedicalClinic"}).text
						clinic_name = " ".join(clinic_name.encode('utf-8').split())
						clinic_list.append(str(clinic_name)+"$")
					except:
						clinic_list.append("NF")

					try:
						clinic_add  = item_map_app.find("div",{"itemtype":"https://schema.org/PostalAddress"}).text
						clinic_add  = " ".join(clinic_add.encode('utf-8').split())
					
						clinic_list.append(str(clinic_add)+"$")
					except:
						clinic_list.append("NF")
					try:
						clinic_coordi = item_map_app.find("div",{"itemtype":"https://schema.org/GeoCoordinates"})
						input_tag = clinic_coordi.find_all("input")
						lat = input_tag[0]['value']
						lon = input_tag[1]['value']
						# print lat,lon
						clinic_list.append("lat :"+str(lat))
						clinic_list.append("lon :"+str(lon)+"$$")
					except:
						clinic_list.append("lat :"+"NF")
						clinic_list.append("lon :"+"NF"+"$$")



					

				doc_info.update({"clinic_list":clinic_list})



				doc_info['doc_deg_list'] = MySQLdb.escape_string(remove_xc2(str(doc_info['doc_deg_list'])))
				doc_info['doc_summ'] = MySQLdb.escape_string(remove_xc2(str(doc_info['doc_summ'])))
				doc_info['Languages'] = MySQLdb.escape_string(remove_xc2(str(doc_info['Languages'])))
				doc_info['Expertise'] = MySQLdb.escape_string(remove_xc2(str(doc_info['Expertise'])))
				doc_info['Qualifications'] = MySQLdb.escape_string(remove_xc2(str(doc_info['Qualifications'])))
				doc_info['Certifications and Memberships'] = MySQLdb.escape_string(remove_xc2(str(doc_info['Certifications and Memberships'])))
				doc_info['Experience'] = MySQLdb.escape_string(remove_xc2(str(doc_info['Experience'])))
				doc_info['Consultation fee'] =  MySQLdb.escape_string(remove_xc2(str(doc_info['Consultation fee'])))
				doc_info['Awards and publication'] = MySQLdb.escape_string(remove_xc2(str(doc_info['Awards and publication'])))
				doc_info['Professional Experience'] = MySQLdb.escape_string(remove_xc2(str(doc_info['Professional Experience'])))
				doc_info['clinic_list'] = MySQLdb.escape_string(remove_xc2(str(doc_info['clinic_list'])))
				doc_info['doc_type_list'] = MySQLdb.escape_string(remove_xc2(str(doc_info['doc_type_list'])))

				sql1 = "INSERT INTO `hel_doc_info2`( `Name`, `Recommemdation`, `Doc_link`, `Image-link`, `personal_link`, `Degree`,"
				sql2 = " `Speciality`, `Summary`, `Languages`, `Expertise`, `Qualifications`, `Certifications_n _Mem`, `Experience`, "
				sql3 = "`Consultation_fee`, `Awards_n_publi`, `Professional_Exp`, `clinic_infos`, `specs_script`, `Location`, `City`) VALUES ("
				sql4 = '"'+ doc_info["doc_name"] + '"' +',"'+doc_info['recommen']+'"'+',"'+doc_link+'"'+',"'+doc_info['img_src']+'"'+',"'+doc_info['prsnl_link']+'"'
				sql5 = ',"'+doc_info['doc_deg_list']+'"'+',"'+doc_info['doc_type_list']+'"'+',"'+doc_info['doc_summ']+'"'+',"'+doc_info['Languages']+'"'
				sql6 = ',"'+doc_info['Expertise']+'"'+',"'+doc_info['Qualifications']+'"'+',"'+doc_info['Certifications and Memberships']+'"' 
				sql7 = ',"'+doc_info['Experience']+'"'+',"'+doc_info['Consultation fee']+'"'+',"'+doc_info['Awards and publication']+'"'
				sql8 = ',"'+doc_info['Professional Experience']+'"'+',"'+doc_info['clinic_list']+'"'+',"'+str(spec)+'"'+',"'+str(item_locality)+'"'+',"'+str(city)+'"'+ ')'

				
				sql = sql1 + sql2 +sql3+ sql4 + sql5 +sql6 +sql7 + sql8
				cursor.execute(sql)
				db.commit()

				print "########################################"
			# print doc_info


