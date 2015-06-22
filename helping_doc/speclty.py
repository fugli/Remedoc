from bs4 import BeautifulSoup

srcpage = open("src_pg.html","r")

soup = BeautifulSoup (srcpage)

atag = soup.find_all("option")
# print >> open ("speciality_ylw_pgs.txt","w"),""
for item in atag:
	print >> open ("city.txt","a")," ".join(item.text.encode('utf-8').split())

print soup.prettify()