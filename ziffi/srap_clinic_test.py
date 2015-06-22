
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


db = MySQLdb.connect("localhost","root","8520","Ziffi")
cursor = db.cursor()


def fn (url):
	req = urllib2.Request(url)#, headers=hdr)
	html_page = urllib2.urlopen(req).read()
	soup = BeautifulSoup(html_page)
	p = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
	return soup

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
	return TAG_RE.sub('', text)

xc_rem = re.compile(r',*\xc2\xa0')
def remove_xc2(text):
	return xc_rem.sub('', text)



flag_item = 0
c = ['hyderabad']
for i in range(0,1):
	print c[i]
	clinic_link = open('clinics_%s_link.html'%c[i],'r').readlines()
	for item in clinic_link:
		flag_err404 = 0
		clinic_url = item
		item = item.rstrip()
		
		if item == 'https://www.ziffi.com/hospitals-in-hyderabad/preetis-rehab-banjara-hills/':
			flag_item = 1
		elif flag_item==0:
			continue
		print item
		while True :
			try :
				soup1 = fn(item)
			except urllib2.HTTPError,err:
				if err.code == 404:
					flag_err404 = 1
					break
				print "loops until err is solved"
				continue
			else:
				break
		# soup1 = fn('https://www.ziffi.com/hospitals-in-bangalore/columbia-asia-referral-hospital-yeshwanthpur/')
		if flag_err404 == 1:
			continue
		clinic_info ={}
		section_blk_1 = soup1.find("div",{"class":"profile-brief-info section-block"})
		####img src
		img_src = section_blk_1.find("div",{"class":"profile-photo-block"}).img['src']
		clinic_info.update({'img_src':img_src})

		###generalinfo
		div_general = section_blk_1.find("div",{"class":"columns small-8 medium-10 end"})
		####clinic name
		clinic_name = div_general.find("h1",{"class":"profile-name-result"}).text
		clinic_name = " ".join(clinic_name.encode('utf-8').split())
		clinic_info.update({'clinic_name':clinic_name})

		####rating
		try:
			div_rate = div_general.find("a",{"class":"rating"})
			overall_rate = div_rate['data-rating']
			num_review = div_rate.find("span",{"itemprop":"count"}).text
			clinic_info.update({'num_review':num_review , 'overall_rate':overall_rate})
		except:
			print 'review NF'
			clinic_info.update({'num_review':"NF" , 'overall_rate':'NF'})

		# print overall_rate,num_review

		####brief info abt clinic
		try:
			brief_info = div_general.find("div",{"class":"result-elements sub-text"}).text
			brief_info = " ".join(remove_xc2(brief_info).encode('utf-8').split())
			clinic_info.update({'brief_info':brief_info})
		except:
			print 'brief info NF'
			clinic_info.update({'brief_info':'NF'})


		####address
		clinic_add = div_general.find("a",{"class":"hospital-address-btn"})['data-address']
		clinic_add = clinic_add.replace('"',"'")
		clinic_info.update({'clinic_add':clinic_add})

		####time table #doc
		div_tim_doc = div_general.find_all("div",{"class":"small-12 medium-4 columns"})
		time = " ".join(remove_xc2(div_tim_doc[0].text).encode('utf-8').split())
		clinic_info.update({'time':time})

		doc_num = " ".join(remove_xc2(div_tim_doc[1].text).encode('utf-8').split()) 
		clinic_info.update({'doc_num':doc_num })

		# print len(div_tim_doc)


		####diagnostic test
		
		####tests
		try:	
			clinic_info.update({'tests':'NF'})
			tests = []
			for num in range(1,500):
				# item = 'https://www.ziffi.com/hospitals-in-bangalore/columbia-asia-referral-hospital-yeshwanthpur/'
				url = item + 'packages-page-'+str(num)+'/'
				print url 
				while True:
					try:
						soup3 = fn(url)
					except:
						print 'line 119 loops until err is solved'
					else:
						break

				section_blk_2 = soup3.find("div",{"class":"packages-block section-block"})
				diag_test_li = section_blk_2.find_all("div",{"class":re.compile(r'medium-6')})#"small-12""medium-6"
				# clinic_info.update
				
				for item_diag_test in diag_test_li:
					test_row = item_diag_test.find('div',{'class':'row'})
					test_title = test_row.find('div',{'class':'columns'})
					title = ' '.join(test_title.text.encode('utf-8').split())
					tests.append(str(title)+'$')
					link = test_title.a['href']
					# print link
					while True:
						try:
							soup2 = fn(link)
						except:
							print 'line 138 looping'
						else:
							break

					test_ul = soup2.find('ul',{'class':'tests-list-full collapsible'})
					for item_testli in test_ul.find_all('li'):
						test_name = ' '.join(item_testli.text.encode('utf-8').split())
						if test_name=='\xc2\xa0':
							break
						tests.append(test_name)

					# test_name_li = (test_row.find('div',{'class':'small-8 columns'})).find_all('li',{'class':'trimmed'})
					
					# for item_testname in test_name_li:
					# 	test_name = ' '.join(item_testname.text.encode('utf-8').split())
					# 	if test_name=='\xc2\xa0':
					# 		break
					# 	tests.append(test_name)
					
					div_cost = test_row.find('div',{'class':'package-cost-section'})
					cost = ' '.join(div_cost.text.encode('utf-8').split())
					tests.append(str(cost))
					tests.append('$$')
				# print tests
				# print  '###'
				clinic_info.update({'tests':tests})
		except:
			print 'empty'
			# clinic_info.update({'tests':'NF'})

		##about clinic
		flag_about = 0
		flag_stats = 0
		div_about = soup1.find('div',{'class':'about-block section-block'})
		div_aboutrow = div_about.find_all('div',{'class':'row'})
		divs = (div_aboutrow[1]).find_all('div')
		about=[]
		stats ={}
		# print divs
		for item_divs in divs:
			try:
				
				if flag_about == 0:
					for ptag in  item_divs.find_all('p') :
						text = remove_xc2(ptag.text.encode('utf-8'))
						flag_about =1
						# print "in about"
						about.append(text)
					clinic_info.update({'about':about })

			except :
				print 'about'
				pass
			try:
				if flag_stats ==0:

					tr = item_divs.find_all('tr')
					# print tr
					for item_row in tr:
						key = ' '.join(item_row.th.text.encode('utf-8').split())
						value = ' '.join(item_row.td.text.encode('utf-8').split())

						stats.update({key:value})
						# print 'in stats'
						flag_stats = 1
			except:
				print 'line 111'
				pass
		clinic_info.update({'stats':stats})

		# print about
		# print stats
		####Gallery 
		try:
			div_gallery = soup1.find('div',{'class':'gallery-container text-center'})
			images_li = div_gallery.find_all('img')
			imgs = []
			for item_img in images_li:
				imgs.append(item_img['src'])
			clinic_info.update({'imgs':imgs })
		except :
			print 'images'
			clinic_info.update({'imgs':'NF'})


		####maps
		location = {}
		div_map = soup1.find('div',{'id':'google-map'})
		lat = div_map['data-lat']
		lng = div_map['data-lng']
		location.update({"lat":lat,'lng':lng})
		# print location
		clinic_info.update({'location':location })

		# print len(diag_test_li)
		# print (clinic_info)
		company = {}
		try:
			div_insu = soup1.find('div',{'class':'insurances-block section-block'})
			div_classes = div_insu.find_all('div',{'class':'columns'})
			
			for item_insu in div_classes:
				h4_tag = item_insu.find('h4')
				if h4_tag:
					try:
						insu_title = ' '.join(h4_tag.text.encode('utf-8').split())
						comp_list = []
						for item_comp in item_insu.find_all('li'):
							comp_list.append(' '.join(item_comp.text.encode('utf-8').split()))
						company.update({insu_title:comp_list})
					except:
						company.update({insu_title:'NF'})
		except:
			company.update({'Third Party Administrators (TPAs)':'NF'})
			company.update({'Insurances':'NF'})

		# print company

		# print clinic_info['clinic_add']
		clinic_info['stats']= MySQLdb.escape_string(remove_xc2(str(clinic_info['stats'])))
		clinic_info['tests']= MySQLdb.escape_string(remove_xc2(str(clinic_info['tests'])))
		clinic_info['about']= MySQLdb.escape_string(remove_xc2(str(clinic_info['about'])))
		clinic_info['imgs']= MySQLdb.escape_string(remove_xc2(str(clinic_info['imgs'])))
		clinic_info['time'] = MySQLdb.escape_string(remove_xc2(str(clinic_info['time'])))
		clinic_info['clinic_name'] = MySQLdb.escape_string(remove_xc2(str(clinic_info['clinic_name'])))
		try:
			clinic_info['clinic_add'] = MySQLdb.escape_string(remove_xc2(str(clinic_info['clinic_add'])))
		except:
			pass
		clinic_info['location']= MySQLdb.escape_string(remove_xc2(str(clinic_info['location'])))
		company['Third Party Administrators (TPAs)']= MySQLdb.escape_string(remove_xc2(str(company['Third Party Administrators (TPAs)'])))
		company['Insurances']= MySQLdb.escape_string(remove_xc2(str(company['Insurances'])))


		sql1 = 'INSERT INTO `clinic_ziffi`( `Name`, `clinic_imgsrc`, `overall_rating`, `NoOfReviews`, `brief_info`,' 
		sql2 = '`Address`, `NoOfDoc`, `Timing`, `Diagnostic_test`, `About`, `Stats`, `Location`, `Images`, `TPAs(thirdPartyAdmins)`,'
		sql3 = ' `Insurances`, `Clinic_URL`) VALUES ('
		sql4 = '"'+clinic_info['clinic_name'] + '"'+',"'+clinic_info['img_src']+'"'+',"'+clinic_info['overall_rate']+'"'
		sql5 = ',"'+clinic_info['num_review']+'"'+',"'+clinic_info['brief_info']+'"'+',"'+clinic_info['clinic_add']+'"'
		sql6 = ',"'+clinic_info['doc_num']+'"'+',"'+clinic_info['time']+'"'+',"'+clinic_info['tests']+'"'+',"'+clinic_info['about']+'"'
		sql7 = ',"'+clinic_info['stats']+'"'+',"'+clinic_info['location'] +'"'+',"'+clinic_info['imgs']+'"'
		sql8 = ',"'+company['Third Party Administrators (TPAs)']+'"'+',"'+company['Insurances']+'"'+',"'+clinic_url+'"'+')'

		
		sql = sql1+sql2+sql3 +sql4+sql5+sql6+ sql7+sql8
		# print sql
		cursor.execute(sql)
		db.commit()

		print "########"
	