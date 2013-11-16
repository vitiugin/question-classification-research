# -*- coding: utf-8 -*-
import re
import csv
import codecs

import nltk
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

# ----------------------------------------------------------------
def replace_two_or_more(s):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

def process_question(question):
    question = question.lower()
    question = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',question)
    question = re.sub('[\s]+',' ',question)
    question = question.strip('\'"')
    return question

def get_stop_word_list(stop_word_list_file_name):
    stop_words = []
    stop_words.append('URL')
    fp = open(stop_word_list_file_name, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stop_words.append(word)
        line = fp.readline()
    fp.close()
    return stop_words
    
def get_feature_vector(question, stop_words):
    prefeature_vector = []
    feature_vector = []
    words = question.split()
    for w in words:
        w = replace_two_or_more(w)
        w = w.strip('\'"?,.')
        val = re.search(r"^[а-яА-Я][а-яА-Я0-9]*$", w)
        if(w in stop_words or val is None):
            continue
        else:
            prefeature_vector.append(w.lower())
    for w in prefeature_vector:
        reel = w.decode('utf-8')
        a = morph.parse(reel)    
        for g in a[:1]:
            w = g.normal_form
            feature_vector.append(w.lower())
    
    return feature_vector
    
def get_feature_list(file_name):
    fp = open(file_name, 'r')
    line = fp.readline()
    feature_list = []
    while line:
        line = line.strip()
        feature_list.append(line)
        line = fp.readline()
    fp.close()
    return feature_list
    
def extract_features(question):
    question_words = set(question)
    features = {}
    for word in feature_list:
        features['contatins(%s)' % word] = (word in question_words)
    return features   
        

inp_questions = csv.reader(open('Data/sampleQuestions_RU.csv', 'rb'), delimiter=',', quotechar = '|')
stop_words = get_stop_word_list('Data/stopwords_RU.txt')
feature_list = get_feature_list('Data/sampleQuestionFeatureList_RU_lem.txt')

questions = []
for row in inp_questions:
    classType = row[0]
    question = row[1]
    processedQuestion = process_question(question)
    featureVector = get_feature_vector(processedQuestion, stop_words)
    questions.append((featureVector, classType))
    
training_set = nltk.classify.util.apply_features(extract_features, questions)

bnc_classifier = nltk.NaiveBayesClassifier.train(training_set)

test_question = ["	как могла сложиться судьба Митраши и Насти в рассказе Кладовая солнца?	"	,
"	в чем идея пьесы старший брат	"	,
"	Почему цензура назвала рассказ А. П. Платонова 'Возвращение' клеветой? На кого? Почему?	"	,
"	где скачать в интернете учебник: Григорьев	"	,
"	Какую литературу порекомендуете новичку на бирже?	"	,
"	как понять: его очередная саба?	"	,
"	какие блог платформы позволяют писать книги?	"	,
"	про что рассказывается в черной книге?	"]

for ask in test_question:
    processed_test_question = process_question(ask)
    print bnc_classifier.classify(extract_features(get_feature_vector(processed_test_question, stop_words)))


