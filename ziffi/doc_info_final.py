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

print >> open("clinics_hyderabad_link.html",'a'),""
print >> open("doc_hyderabad_link.html",'a'),""
db = MySQLdb.connect("localhost","root","8520","Ziffi")
cursor = db.cursor()

def fn (url):
	req = urllib2.Request(url)
	html_page = urllib2.urlopen(req)#.read()
	soup = BeautifulSoup(html_page)
	finalurl = html_page.geturl()
	return [soup,finalurl]
flagspec =0
flagnum = 0
flagloc = 0

# soup1 = BeautifulSoup(open("htmlpgsrc.html"))
city = "hyderabad"													 #####to be changed 1
####mumbai
# locality = ['bandra','lokhandwala','andheri-west','malad-west','andheri-east','thane-west','mira-bhayandar-road','borivali-west','kandivali-west']
###delhi-ncr
# locality = ['gurgaon','vasant-kunj','patparganj','noida','janakpuri','dwarka','tughlaqabad','rohini','faridabad']
###bangalore
# locality = ['koramangala','indira-nagar','maratha-halli','rajajinagar','vasanth-nagar','hsr-layout','malleswaram','jaya-nagar','kalyan-nagar']
locality = ['ameerpet','kphb-colony','banjara-hills','secunderabad','somajiguda','jubilee-hills','kukatpally','gachibowli']
###location to be changed 2

speciality = open("speciality.txt",'r').readlines()
for loc in locality :
	# if loc =="malleswaram":                  #####to be changed 3
	# 	flagloc =1
	# 	print "found the location"
	# elif flagloc ==0:
	# 	continue

	for speclty in speciality:
		speclty = ("-".join(speclty.split())).lower()
		print speclty
		if speclty =="dermatology-(skin)":                  #####to be changed 3
			flagspec =1
			print "found the soeclty"
		elif flagspec ==0:
			continue

		if speclty == "cervical-disc/-surgery-for-cervical-spondylosis:":         #####to be changed 3
			speclty = "Cervical-disc-surgery"
		
		flag_url = 1
		for num in range(1,200):
			# if num == 55:
			# 	flagnum =1
			# elif flagnum ==0:
			# 	continue        										 #####to be changed 4
			if flag_url ==0:
				break

			if num==1 :
				suburl1 = "https://www.ziffi.com/doctors-in-%s/"%str(city)+speclty+"/"+str(loc)+"/"   #####to be changed 4 city

			url1 = suburl1+"page-"+str(num)+"/"
			print url1
			try:
				ret_soup1 = fn(url1)
				soup1 = ret_soup1[0]
				finalurl = ret_soup1[1]
			except:
				print "######WEBSITE NOT FOUND"
				break
			
			if num ==1 :
				suburl1 = finalurl

			print finalurl
			print "$$$$$"
			if finalurl == url1 or num==1 :
				flag_url =1
			else:
				flag_url = 0

			if flag_url == 1 :
				
				pg_cntanr = soup1.find("div",{"id":"search-page-container"})
				div_row = pg_cntanr.find_all("div",{"class":"row"})

				total_res = div_row[0].find("span").text.encode('utf-8')
				print total_res

				div_row_doclist = div_row[1].find_all("div",{"class":"z-card"})
				# print div_row_doclist

				
				for item in div_row_doclist:
					doc_info_dict = {}

					info_cntanr = item.find("div",{"class":["small-12"," medium-8","columns"]})
					prof_detail = info_cntanr.find("div",{"class":"profile-details"})
					# print prof_detail

					#####prof detail name ,href 
					h2_prof_name = prof_detail.find("h2")
					doc_href = h2_prof_name.a['href']
					name = h2_prof_name.text.encode('utf-8')
					doc_info_dict.update({"doc_href":doc_href,"name":name})
					print doc_info_dict["doc_href"]
					
					#####doc deg
					try:
						doc_deg = prof_detail.find("p").text.encode('utf-8')
						doc_info_dict.update({"doc_deg":doc_deg})
					except:
						# print "no doc_degfound"
						doc_info_dict.update({"doc_deg":"NF"})

					exp_typdoc = prof_detail.find_all("div",{"class":"result-elements"})

					#####doc type
					try:
						type_doc = exp_typdoc[0].text.encode('utf-8')
						type_doc = " ".join(type_doc.split())
						doc_info_dict.update({"type_doc":type_doc})
					except:
						# print "type NF"
						doc_info_dict.update({"type_doc":"NF"})

					#####doc experience
					try:
						exp_yrs = exp_typdoc[1].text.encode('utf-8')
						doc_info_dict.update({"type_doc":type_doc,"exp_yrs":exp_yrs})
					except:
						# print"exp NF"
						doc_info_dict.update({"exp_yrs":"NF"})


					#####clinics under doc
					doc_clinics = prof_detail.find("ul",{"class":"no-bullet"})
					clinc_list = doc_clinics.find_all("li",{"class":"search-doctor-hospital-list-item"})
					all_clinics_infos = []
					for item2 in clinc_list:
						one_clinic_info = []
						try:
							atag = item2.find("a")
							clinic_href = atag['href']
							
							link_file = open("clinics_hyderabad_link.html","r").readlines()
							if not (str(clinic_href)+'\n') in link_file:
								print >> open("clinics_hyderabad_link.html",'a'),clinic_href

							one_clinic_info.append(clinic_href)

							clinic_name = atag.text.encode('utf-8')
							one_clinic_info.append(clinic_name)

							locality = item2.find("span").text.encode('utf-8')
							one_clinic_info.append(locality)

							all_clinics_infos.append(one_clinic_info)

							
						except:
							pass

					doc_info_dict.update({"all_clinics_infos":all_clinics_infos})
					# print doc_info_dict
					# print "######"+'\n'

					####popular specialists
					try:
						all_docpop = []
						doc_info_dict.update({"pop_doc":"NF"})
						ul_popular = soup1.find("ul",{"class":"content-slider-ls no-bullet"})
						li_popular = ul_popular.find_all("li")
						for item_pop in li_popular:
							one_docpop = []
							div_pop = item_pop.find("div",{"class":"doctor-brief-profile-container text-center"})
							doc_pop_url = div_pop.a['href']
							pop_rev = item_pop.find("div",{"class":"text-hover image-hover"})
							num_rev = pop_rev.text.encode('utf-8')
							try:
								star = len(pop_rev.find_all("span",{"class":"on"}))
							except:
								star = "No star"
							one_docpop.append(" ".join(num_rev.split()))
							one_docpop.append(str(star)+" stars")
							one_docpop.append(doc_pop_url)
							all_docpop.append(one_docpop)

						# print star,doc_pop_url,num_rev
						doc_info_dict.update({"pop_doc":all_docpop})

					
					except:
						pass
					
					# print doc_info_dict["pop_doc"]
					# print "******************************"


					###################SECOND LEVEL##################
					url2 = doc_info_dict['doc_href']
					# url2= 'https://www.ziffi.com/doctors-in-mumbai/mona-kukreja-gynecology/'        #####to be changed 5 done
					doc_detail = {}
					doc_link_file =open ("doc_hyderabad_link.html",'r').readlines()
					if not (str(url2)+'\n') in doc_link_file:
						print >> open("doc_hyderabad_link.html",'a'),url2
						
						ret_soup2 = fn(url2)
						soup2 = ret_soup2[0]

						

						div_prof_photo = soup2.find("div",{"class":"profile-photo-block"}).img['src']
						doc_detail.update({"div_prof_photo":div_prof_photo})
						

						div_profcntanr = soup2.find("div",{"class":"profile-info-container"})

						#### brief infos
						divtag_resele = div_profcntanr.find_all("div",{"class":"result-elements"})
						# spec = " ".join(divtag_resele[0].text.encode('utf-8').split())
						# doc_detail.update({"spec":spec})
						doc_detail.update({"fees":"NF"})
						doc_detail.update({"langs":"NF"})

						for div_item in divtag_resele:
							####fees
							if div_item.find("a",{"class":"private-info-trigger"}):
								try:
									fees = div_item.a['data-fees']
									doc_detail.update({"fees":fees})
								except:
									doc_detail.update({"fees":"NF"})
							####lang
							elif div_item.find("i",{"class":"fa fa-language"}):
								try:
									spantag_lang = div_item.find_all("span")
									langs = []
									for item in spantag_lang:
										langs.append(item.text.encode('utf-8'))

									doc_detail.update({"langs":langs})
								except:
									doc_detail.update({"langs":"NF"})


						#####more info section
						div_blocks = soup2.find_all("div",{"class":"row section-block"})
						# print div_blocks
						try:
							spec_moreinfos = div_blocks[0].find("div",{"class":"small-9 medium-10 columns fade-container"}).text.encode('utf-8')
							doc_detail.update({"spec_moreinfos":spec_moreinfos})
						except:
							doc_detail.update({"spec_moreinfos":"NF"})

						try:
							pos_moreinfos = div_blocks[0].find("div",{"class":"small-9 medium-10 columns fade-container doctor-position"}).text.encode('utf-8')
							doc_detail.update({"pos_moreinfos":pos_moreinfos})
						except:
							doc_detail.update({"pos_moreinfos":"NF"})

						doc_detail.update({"Expertise":"Nf"})
						doc_detail.update({"Qualification":"Nf"})
						doc_detail.update({"Research":"Nf"})
						doc_detail.update({"photo_link":"NF"})

						for item in div_blocks[1:]:
							heading = item.find("h2",{"class" :"z-primary-color"}).text.encode('utf-8')

							if heading == "Photos":
								try:
									photo_link = []
									for li_photos in item.find_all("li",{"class":"gallery-item "}):   #thereis aspacechar
										photo_link.append(li_photos.img['src'])
									doc_detail.update({"photo_link":photo_link})
								except:
									doc_detail.update({"photo_link":"NF"})
								# print photo_link

							elif heading == "Directions":
								# print "Directions"
								continue
								# div_map = item.find("div",{"id":"google-map"})
								# # print div_map
								# lat = div_map['data-lat']
								# lon = div_map['data-lng']
								# print lat,lon
							else:
								try:
									lists_heading = [] 
									for li_item in item.find_all("li",{"class":""}):
										lists_heading.append(li_item.text.encode('utf-8'))
									doc_detail.update({heading:lists_heading})
								except:
									doc_detail.update({heading:"NF"})

								# print heading
								# print lists_heading

						try:
							doc_detail.update({"review":"NF"})
							all_rev = []
							div_reviews = soup2.find("div",{"class":"review-block section-block"})
							block_quotes = div_reviews.find_all("blockquote",{"itemprop":"review"})
							for item_quotes in block_quotes:
								one_rev = []
								review = item_quotes.find("p",{"itemprop":"description"}).text
								review = " ".join(review.encode('utf-8').split())
								rev_star = item_quotes.find("div",{"class":"text-right"})
								star = len(rev_star.find_all("span",{"class":"on"}))
								one_rev.append(review)
								one_rev.append(star)
								all_rev.append(one_rev)
								# print star
								# print review
							doc_detail.update({"review":all_rev})
						except:
							# print "NO REVIEW"
							doc_detail.update({"review":"NF"})
						# print doc_detail["review"]


						# print doc_detail

						doc_info_dict["all_clinics_infos"] = MySQLdb.escape_string(str(doc_info_dict["all_clinics_infos"]))
						doc_info_dict["pop_doc"] = MySQLdb.escape_string(str(doc_info_dict["pop_doc"]))
						doc_detail["Expertise"] = MySQLdb.escape_string(str( doc_detail["Expertise"]))
						doc_detail["Qualification"] = MySQLdb.escape_string(str(doc_detail["Qualification"]))
						doc_detail["langs"] = MySQLdb.escape_string(str(doc_detail["langs"]))
						doc_detail["fees"] = MySQLdb.escape_string(str(doc_detail["fees"]))
						doc_detail["photo_link"] = MySQLdb.escape_string(str(doc_detail["photo_link"]))
						doc_detail["review"] = MySQLdb.escape_string(str( doc_detail["review"]))

						sql1 = "INSERT INTO `ziffi_doc_info`( `Name`, `Degree`, `Exp`, `Type_doc`, `Doc_link`, `Available_at`, `Expertise`, `Qualification`, `Doc_Photo_link`, `Fees`, `Lang`,`Specialities`, `Position`, `speclty_script`, `locality_script`, `City`, `Link`, `All_clinics_photolink`,`Reviews`,`Popular`) VALUES ("
						sql2 = '"'+doc_info_dict["name"]+'"'+',"'+doc_info_dict["doc_deg"]+'"'+',"'+doc_info_dict["exp_yrs"]+'"'+',"'+doc_info_dict["type_doc"]+'"'
						sql3 = ',"'+doc_info_dict["doc_href"]+'"'+',"'+doc_info_dict["all_clinics_infos"]+'"'+',"'+doc_detail["Expertise"]+'"'+',"'+doc_detail["Qualification"]+'"'
						sql4 = ',"'+doc_detail["div_prof_photo"]+'"'+',"'+doc_detail["fees"]+'"'+',"'+doc_detail["langs"]+'"'+',"'+doc_detail["spec_moreinfos"]+'"'+',"'+doc_detail["pos_moreinfos"]+'"' 
						sql5 = ',"'+speclty +'"'+',"'+ loc +'"'+',"'+city +'"'+',"'+ url1+'"'+',"'+doc_detail["photo_link"]+'"'+',"'+doc_detail["review"]+'"'+',"'+doc_info_dict["pop_doc"]+'"'+ ")"
						sql = sql1+sql2+sql3+sql4+sql5
						cursor.execute(sql)
						db.commit()
						print "######@@@@@@@@@@@@"


					



