from bs4 import BeautifulSoup
import urllib2
import re
import csv

mainurl = "http://www.courts.ca.gov/opinions-slip.htm?Courts=R"

page = urllib2.urlopen(mainurl).read()
soup = BeautifulSoup(page, "html.parser")

mainurl = soup.find("iframe", id="frame-content")
mainurl = mainurl.a["href"]

page = urllib2.urlopen(mainurl).read()
soup = BeautifulSoup(page, "html.parser")
table = soup.find("table", {"border" : "0"})

pdf_begin = "http://www.courts.ca.gov"

csv_file = open('CA.csv', 'wb')
head = ['Date Posted', 'Case Number', 'Description', 'PDF Link']
csv_writer = csv.writer(csv_file)
csv_writer.writerow(head)
for row in table.findAll("tr")[1:]:
    content = []
    [date, fname, description] = row.findAll("td")
    date = date.text.strip()
    pdf_url = pdf_begin + fname.a["href"]
    fname = fname.text.strip()[:-11]
    description = (description.text.strip()[:-15]).encode('utf-8')
    content.append((date, fname, description, pdf_url))
    try:
        print 'downloading', pdf_url, '...'
        f = open(fname + '.pdf', 'wb')
        f.write(urllib2.urlopen(pdf_url).read())
        f.close()
        csv_writer.writerows(content)
    except:
        print '(404) not found error, continue...'
        continue
