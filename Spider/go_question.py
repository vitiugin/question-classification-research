# -*- coding: utf-8 -*-

import urllib
import lxml.html
import sys
import re
import codecs

def EveryLink(Link):
    newPage = urllib.urlopen(Link)
    finPage = newPage.read()

    doc = lxml.html.document_fromstring(finPage.decode('utf-8'))

    for question in doc.cssselect('.ttl.row'):
        FinishedLink = question.text_content()
        output_file.write(FinishedLink)
       
def LinkList(ListOfLinks):
    UrlsFile = codecs.open(ListOfLinks, 'r', 'utf-8') 
    UrlsFile = re.split(r'[\n]+', UrlsFile.read())
    for url in UrlsFile:
        EveryLink(url)

output_file = codecs.open('FullListofQuestions.txt', 'w', 'utf-8')

print u'question_list.txt'
LinkList('question_list.txt')


output_file.close()

