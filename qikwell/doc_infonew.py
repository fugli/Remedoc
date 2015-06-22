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


def fn (url):
	html_page = urllib2.urlopen(url)
	soup = BeautifulSoup(html_page)
	return soup

soup = BeautifulSoup (open('srcpg.html'))

doc_info = {}
prof = soup.find('div',{'class':'profile clearfix col-lg-8 col-md-8 col-sm-8 col-xs-12'})
div_left = prof.find('div',{'class':'left'})
###image link
try:
	div_img = div_left.find('div',{'class':'img-holder'})
	docimage_link = div_img.img['src']
	doc_info.update({'docimage_link':docimage_link})
except:
	print 'no img'
	doc_info.update({'docimage_link':docimage_link})
###fees
try:
	div_fees = div_left.find('div',{'class':'fees'})
	fees = ' '.join(div_fees.text.encode('utf-8').split())
	doc_info.update({'fees':fees})
except:
	doc_info.update({'fees':"NF"})
	print 'No fees'

div_right = prof.find('div',{'class':'right'})
###doc name
name = div_right.find('h1',{'class':'name'})
name =' '.join(name.text.encode('utf-8').split())
doc_info.update({'name':name})
###info

info = div_right.find('div',{'class':"info"})
# print info
###specality
div_spec = info.find('h2',{'class':'speciality'})
speciality =' '.join( div_spec.text.encode('utf-8').split())
####
qualif = info.find('span',{'class':'doctor_qualification'})
qualif = ' '.join(qualif.text.encode('utf-8').split())
####ecoomendation
try:
	heart_itag = info.find('i',{'class':'qicon-heart'})
	par_itag  = heart_itag.parent
	recomm = ' '.join(par_itag.text.encode('utf-8').split())
	doc_info.update({'recomm':recomm})
	
except:
	doc_info.update({'recomm':"recomm"})
# ###languages
# lang = info.find('span',{'class':'text lang_text'})
# print lang
# lang =' '.join(lang.text.encode('utf-8').split())
# doc_info.update({'lang':lang})

sec2 = soup.find('section',{'class':'two-column statement-location'})
div_loc = sec2.find('div',{'class':'location col col-sm-6 col-xs-12'})
div_cl_li = div_loc.find('div',{'class':'clinics-list'})
clinic_info_list = []
for item_li in div_cl_li.find_all('div',{'class':'clinic'}):
	clinic_info = []
	div_name = item_li.find('div',{'class':'name'})
	clinic_link = div_name.a['href']
	name = div_name.text.encode('utf-8')
	clinic_info.append(name)
	clinic_info.append(clinic_link)
	div_add = item_li.find('div',{'class':'address'})
	street_add = div_add.find('span',{'itemprop':'streetAddress'}).text.encode('utf-8')
	add_loclty =  div_add.find('span',{'itemprop':'addressLocality'}).text.encode('utf-8')
	ad_region = div_add.find('span',{'itemprop':'addressRegion'}).text.encode('utf-8')
	pin_code =  div_add.find('span',{'itemprop':'postalCode'}).text.encode('utf-8')
	clinic_info.extend(['street:'+street_add,'locality:'+str(add_loclty) ,'region:'+str(ad_region), 'pin:'+pin_code])
	# print clinic_info
####teatment offered
sec3 = soup.find('section',{'class':'two-column treatment-affliation'})
# print sec3
treatment = sec3.find('div',{'class':'treatment col first col-sm-6 col-xs-12'})
treat_offerd = []
for item_li in treatment.find_all('li'):
	item = item_li.text.encode('utf-8')
	treat_offerd.append(item)

####affiation
affilia_offerd = []
affiliation = sec3.find('div',{'class':'affiliation col last col-xs-12 col-sm-6'})
for item_li in affiliation.find_all('li'):
	item = item_li.text.encode('utf-8')
	affilia_offerd.append(item)
print affilia_offerd
print treat_offerd
# print doc_info


