# -*- coding: utf-8 -*-

import re
import csv
import codecs

import pymorphy2

morph = pymorphy2.MorphAnalyzer()

# ------------------preprocess.py---------------------------
# первоначальная обработка вопросов
def process_question(question):
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
stop_words = []

# функция удаление повторяющихся сивовол replaceTwoOrMore
def replace_two_or_more(s):
    # поиск 2 и более повторяющихся символов
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

# функция получание стоп-слов
def get_stop_word_list(stop_word_list_file_name):
    # подгрузка стоп-слов из файла и создание списка
    stop_word = []
    stop_word.append('URL')
    
    fp = open(stop_word_list_file_name, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stop_word.append(word)
        line = fp.readline()
    fp.close()
    return stop_word

# функция получения векторов признаков
def get_feature_vector(question):
    prefeature_vector = []
    feature_vector = []
    # деление вопроса на слова (простейшая токенизация)
    words = question.split()
    for w in words:
        # удаление повторяющихся символов
        w = replace_two_or_more(w)
        # удаление пуктуационных знаков
        w = w.strip('\'"?,.')
        # проверка наличия слов, начинающихся не с букв
        val = re.search(r"^[а-яА-Я][а-яА-Я0-9]*$", w)
        # игнорирование стоп-слов
        if(w in stop_words or val is None):
            continue
        else:
            prefeature_vector.append(w.lower())
        #лемматизация
    for w in prefeature_vector:
        reel = w.decode('utf-8')
        a = morph.parse(reel)    
        for g in a[:1]:
            w = g.normal_form
            feature_vector.append(w.lower())
    
    return feature_vector
    
#fp = open('Data/training.txt', 'r')
#line = fp.readline()

st = open('Data/stopwords_RU.txt', 'r')
stop_words = get_stop_word_list('Data/stopwords_RU.txt')

"""
while line:
    processedQuestion = processQuestion(line)
    featureVector = getFeatureVector(processedQuestion)
    print featureVector
    line = fp.readline()
    
fp.close()
"""
# ------------------- Feature Extraction -----------------------------
inp_questions = csv.reader(open('Data/sampleQuestions_RU.csv', 'rb'), delimiter = ',', quotechar='|')
questions = []

for row in inp_questions:
    class_type = row[0]
    question = row[1]
    processed_question = process_question(question)
    featureVector = get_feature_vector(processed_question)
    questions.append((featureVector, class_type))
    
# --------------------------------------------------------------------

# ---------------- Feature List -------------------------
feature_list = []
for words in questions:
    for inner_word in words[0]:
        feature_list.append(inner_word)
        
output_file = codecs.open('Data/sampleQuestionFeatureList_wRU_lem.txt', 'w', 'utf-8')
#codecs.open('corpus_len.txt', 'w', 'utf-8')
for single_feature in feature_list:
    output_file.write("%s\n" % single_feature)
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
    
    
    
    
    
