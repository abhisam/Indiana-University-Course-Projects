import urllib
import re
import csv

if __name__ == '__main__':
    inMainUrl = 'http://www.in.gov'
    htmlurl = inMainUrl + '/judiciary/opinions/archsup.html'
    utfHtml = urllib.urlopen(htmlurl).read()
    colNames = re.findall(r'<th.*?<font face="Arial, Helvetica, sans-serif".*?>(.*?)</font>', utfHtml, re.S)
    matchPdfs = re.findall(r'<td scope="row".*?<font face="Arial, Helvetica, sans-serif".*?>(.*?)</font>.*?<a href="(.*?)">(.*?)</a>.*?size="2">(.*?)</font>.*?size="2">(.*?)</font></td>', utfHtml, re.S)
    for col in colNames:
        print col, '|', '\t',

    csv_file = open('IndianaAppellateOpinionsArchive-Supreme-Metadata.csv', 'wb')
    head = ['CaseNumber', 'Date', 'CaseTitle', 'Url', 'LCCN', 'ACCN']
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(head)
    content = []

    for date, link, case, lccn, accn in matchPdfs:
        url = inMainUrl + link
        content.append([num, date, case, url, lccn, accn])
        print('Case name is: %s\nLink is: %s' % (case, link))
            f = open(str(num) + '.pdf', 'wb')
            f.write(urllib.urlopen(url).read())
            f.close()

    csv_writer.writerows(content)
