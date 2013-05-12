# -*- coding: utf-8 -*-

import urllib
import lxml.html
import codecs

list_of_urls = []

def GoogleLinkSpider(adress):
    count = 20
    while count <= 960:
        dop = '&start=' + str(count)
        newadress = adress + dop
        newPage = urllib.urlopen(newadress)
        finPage = newPage.read()
    
        doc = lxml.html.document_fromstring(finPage.decode('utf-8'))
    
        for question in doc.cssselect('.qtl.lft'):
            FinishedLink = 'http://otvety.google.ru' + question.get('href')
            list_of_urls.append(FinishedLink)
    
        count += 20
    
GoogleLinkSpider('URL') #link to page

output_file = codecs.open('question_list.txt', 'w', 'utf-8')
for link in list_of_urls:
    output_file.write("%s \n" % link)
output_file.close() 



