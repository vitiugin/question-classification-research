# -*- coding: utf-8 -*-

import urllib
import codecs

import lxml.html

list_of_urls = []

def read_google(adress):
    count = 20
    while count <= 960:
        dop = '&start=' + str(count)
        newadress = adress + dop
        new_page = urllib.urlopen(newadress)
        fin_page = new_page.read()
    
        doc = lxml.html.document_fromstring(fin_page.decode('utf-8'))
    
        for question in doc.cssselect('.qtl.lft'):
            finished_link = 'http://otvety.google.ru' + question.get('href')
            list_of_urls.append(finished_link)
    
        count += 20
    
read_google('URL') #link to page

output_file = codecs.open('question_list.txt', 'w', 'utf-8')
for link in list_of_urls:
    output_file.write("%s \n" % link)
output_file.close() 



