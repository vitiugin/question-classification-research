# -*- coding: utf-8 -*-

import urllib
import sys
import re
import codecs

import lxml.html

def read_link(Link):
    new_page = urllib.urlopen(Link)
    finPage = new_page.read()

    doc = lxml.html.document_fromstring(finPage.decode('utf-8'))

    for question in doc.cssselect('.ttl.row'):
        finished_link = question.text_content()
        output_file.write(finished_link)
       
def create_link_list(list_of_links):
    urls_file = codecs.open(list_of_links, 'r', 'utf-8')
    urls_file = re.split(r'[\n]+', urls_file.read())
    for url in urls_file:
        read_link(url)

output_file = codecs.open('FullListofQuestions.txt', 'w', 'utf-8')

print u'question_list.txt'
create_link_list('question_list.txt')


output_file.close()

