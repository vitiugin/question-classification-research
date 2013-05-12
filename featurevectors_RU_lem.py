# -*- coding: utf-8 -*-

import csv

# ------------------preprocess.py---------------------------
import re
import codecs
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

# первоначальная обработка вопросов
def processQuestion(question):
    # обработка вопроса
    
    # перевод в нижний регистр
    question = question.lower()
    # замена ссылок на 'URL
    question = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',question)
    # удаление дополнительных пробелов
    question = re.sub('[\s]+',' ',question)
    # удаление кавычек
    question = question.strip('\'"')
    return question
    
# ----------------------------------------------------------

# создание списка стоп-слов
stopWords = []

# функция удаление повторяющихся сивовол replaceTwoOrMore
def replaceTwoOrMore(s):
    # поиск 2 и более повторяющихся символов
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

# функция получание стоп-слов
def getStopWordList(stopWordListFileName):
    # подгрузка стоп-слов из файла и создание списка
    stopWords = []
    stopWords.append('URL')
    
    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords

# функция получения векторов признаков
def getFeatureVector(question):
    prefeatureVector = []
    featureVector = []
    # деление вопроса на слова (простейшая токенизация)
    words = question.split()
    for w in words:
        # удаление повторяющихся символов
        w = replaceTwoOrMore(w)
        # удаление пуктуационных знаков
        w = w.strip('\'"?,.')
        # проверка наличия слов, начинающихся не с букв
        val = re.search(r"^[а-яА-Я][а-яА-Я0-9]*$", w)
        # игнорирование стоп-слов
        if(w in stopWords or val is None):
            continue
        else:
            prefeatureVector.append(w.lower())
        #лемматизация
    for w in prefeatureVector:
        reel = w.decode('utf-8')
        a = morph.parse(reel)    
        for g in a[:1]:
            w = g.normal_form
            featureVector.append(w.lower())
    
    return featureVector
    
#fp = open('Data/training.txt', 'r')
#line = fp.readline()

st = open('Data/stopwords_RU.txt', 'r')
stopWords = getStopWordList('Data/stopwords_RU.txt')

"""
while line:
    processedQuestion = processQuestion(line)
    featureVector = getFeatureVector(processedQuestion)
    print featureVector
    line = fp.readline()
    
fp.close()
"""
# ------------------- Feature Extraction -----------------------------
inpQuestions = csv.reader(open('Data/sampleQuestions_RU.csv', 'rb'), delimiter = ',', quotechar='|')
questions = []

for row in inpQuestions:
    classType = row[0]
    question = row[1]
    processedQuestion = processQuestion(question)
    featureVector = getFeatureVector(processedQuestion)
    questions.append((featureVector, classType))
    
# --------------------------------------------------------------------

# ---------------- Feature List -------------------------
featureList = []
for words in questions:
    for innerWord in words[0]:
        featureList.append(innerWord)
        
output_file = codecs.open('Data/sampleQuestionFeatureList_wRU_lem.txt', 'w', 'utf-8')
#codecs.open('corpus_len.txt', 'w', 'utf-8')
for oneFeature in featureList:
    output_file.write("%s\n" % oneFeature)
output_file.close()
                
# -------------------------------------------------------        

# --------------------------
"""
def extract_features(question):
    question_words = set(question)
    print question_words
    features = {}
    for word in featureList:
        features['contatins(%s)' % word] = (question in question_words)
    return features

extract_features(q)
"""    
    
    
    
    
    
