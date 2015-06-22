from bs4 import BeautifulSoup

srcpage = open("htmlpgsrc.html","r")

soup = BeautifulSoup (srcpage)

atag = soup.find_all("li")
# print >> open ("speciality_ylw_pgs.txt","w"),""
for item in atag:
	print >> open ("mumbai locations.txt","a"),(" ".join(item.text.encode('utf-8').split())).strip(", Mumbai")

print soup.prettify()