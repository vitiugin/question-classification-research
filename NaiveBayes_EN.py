# -*- coding: utf-8 -*-
import re
import csv
import nltk

# ----------------------------------------------------------------
def replaceTwoOrMore(s):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

def processQuestion(question):
    question = question.lower()
    question = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',question)
    question = re.sub('[\s]+',' ',question)
    question = question.strip('\'"')
    return question

def getStopWordList(stopWordListFileName):
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
    
def getFeatureVector(question, stopWords):
    featureVector = []
    words = question.split()
    for w in words:
        w = replaceTwoOrMore(w)
        w = w.strip('\'"?,.')
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
    
def getFeatureList(fileName):
    fp = open(fileName, 'r')
    line = fp.readline()
    featureList = []
    while line:
        line = line.strip()
        featureList.append(line)
        line = fp.readline()
    fp.close()
    return featureList
    
def extract_features(question):
    question_words = set(question)
    features = {}
    for word in featureList:
        features['contatins(%s)' % word] = (word in question_words)
    return features   
        

inpQuestions = csv.reader(open('Data/sampleQuestions.csv', 'rb'), delimiter=',', quotechar = '|')
stopWords = getStopWordList('Data/stopwords.txt')
featureList = getFeatureList('Data/sampleQuestionFeatureList.txt')

questions = []
for row in inpQuestions:
    classType = row[0]
    question = row[1]
    processedQuestion = processQuestion(question)
    featureVector = getFeatureVector(processedQuestion, stopWords)
    questions.append((featureVector, classType))
    
training_set = nltk.classify.util.apply_features(extract_features, questions)

NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

testQuestion = ["	What does INRI stand for when used on Jesus ' cross ?	",
"	CNN is the abbreviation for what ?	",
"	What does S.O.S. stand for ?	",
"	What is the abbreviation for micro ?	",
"	What does ` PSI ' stand for ?	",
"	What musical instrument did Prewitt play in James Jones 's From Here to Eternity ?	",
"	What cocktail do you concoct with whisky and sweet vermouth ?	",
"	How do you say `` fresh '' in Spanish ?	",
"	What movie did Madilyn Kahn star in with Gene Wilder ?	",
"	What type of bridge is the Golden Gate Bridge ?	",
"	What deck of cards includes the Wheel of Fortune 	",
"	What does the Statue of Liberty wear on her feet ?	",
"	What household facility contains a float ball 	",
"	What was the name of Betty Boop 's dog ?	",
"	What are the distinct physical characterstics of the Arabian horse ?	",
"	What is a fear of thunder ?	",
"	What is a fear of bees ?	",
"	What Vladimir Nabokov novel features Professor Humbert in love with a 12-year-old girl ?	",
"	What game do Steve McQueen and Edward G. Robinson play in The Cincinnati Kid ?	",
"	What fastener did Whitcomb Judson patent in 1893 ?	",
"	What does ribavirin consist of ?	",
"	Name the soft drink that is `` number one in the sun . ''	",
"	What is `` the bear of beers '' ?	",
"	Name the operating system that runs on IBM-compatible machines .	",
"	What color of dry wine should be served with veal roasts and chops ?	",
"	Where is your corpus callosum ?	",
"	When Superman needs to get away from it all 	",
"	Which Latin American country is the largest ?	",
"	What was the former residence of Scottish kings in Edinburgh ?	",
"	What country buys 25 percent of the world 's tea exports ?	",
"	What country is the origin of the band the Creeps ?	",
"	What erupts every hour at Yellowstone National Park ?	",
"	What country contains the highest point in South America ?	",
"	What New York City landmark has 168 steps to its crown ?	",
"	Where is the Bulls basketball team based ?	",
"	What 's the second-highest mountain in the world ?	",
"	What country was Erich Honecker the leader of ?	",
"	What eastern state sprouted the first commercial nuclear power plant in the U.S. ?	",
"	What are the three most populated countries in the world ?	",
"	What U.S. city 's skyline boasts the Gateway Arch ?	",
"	Where is Belize located ?	",
"	What southeast Asian country has the Wang River joining the Ping River at Tak ?	",
"	What Italian city of 155 were Leonardo da Vinci 	",
"	On what avenue is the original Saks department store located ?	",
"	Where does the song Anything Goes take place ?	",
"	Where was the first zoo in the U.S. ?	",
"	Where can I read about Chiang Kai-shek ?	",
"	What country borders the most others ?	",
"	Where on the Internet can I get chemicals importers ?	",
"	What was the first country to put a second woman in space ?	",
"	What prison is found in Ossining 	",
"	What country has declared one-fifth of its territory off-limits to Russians ?	",
"	What is the longest river in the United States ?	",
"	What country 's flag is field green ?	",
"	How did serfdom develop in and then leave Russia ?	",
"	How can I find a list of celebrities ' real names ?	",
"	What are liver enzymes ?	",
"	Why do heavier objects travel downhill faster ?	",
"	What did the only repealed amendment to the U.S. Constitution deal with ?	",
"	What is `` Nine Inch Nails '' ?	",
"	What is an annotated bibliography ?	",
"	What 's the Olympic motto ?	",
"	What is the origin of the name ` Scarlett ' ?	",
"	What do Mormons believe ?	",
"	How can I register my website in Yahoo for free ?	",
"	How do they find or choose witnesses to an execution ?	",
"	How do you ask a total stranger out on a date ?	",
"	What is ethology ?	",
"	Where did the term `` 86ed '' come from ?	",
"	What is the nature of learning ?	",
"	What is the Kashmir issue ?	",
"	What does `` extended definition '' mean and how would one write a paper on it ?	",
"	What is titanium ?	",
"	What is a caldera ?	",
"	Why do people get calluses ?	",
"	What are Cushman and Wakefield known for ?	",
"	What is the history of skateboarding ?	",
"	How do I make fuel bricks from recycled newspaper ?	",
"	How do I log on to home page at Headquarters U.S. European Command ?	",
"	What is the origin of head lice ?	",
"	What causes the body to shiver in cold temperatures ?	",
"	What are bear and bull markets ?	",
"	What is `` dew point '' ?	",
"	What is the meaning of Jesus ?	",
"	What contemptible scoundrel stole the cork from my lunch ?	",
"	What team did baseball 's St. Louis Browns become ?	",
"	What is the oldest profession ?	",
"	Name the scar-faced bounty hunter of The Old West .	",
"	Who was The Pride of the Yankees ?	",
"	Who killed Gandhi ?	",
"	Name 11 famous martyrs .	",
"	Who was the inventor of silly putty ?	",
"	Which company that manufactures video-game hardware sells the `` super system '' ?	",
"	What 1920s cowboy star rode Tony the Wonder Horse ?	",
"	What ISPs exist in the Caribbean ?	",
"	Who was the prophet of the Muslim people ?	",
"	Who is Snoopy 's arch-enemy ?	",
"	Who do Herb and Tootsie live next door to ?	",
"	Who is the founder of Scientology ?	",
"	Who starred in Singing in the Rain and The Singing Nun ?	",
"	What 19th-century painter died in the Marquesas Islands ?	",
"	Who were the five Marx brothers ?	",
"	What company 's logo is a `` W '' in a circle ?	",
"	Who invented Make-up ?	",
"	Which of the following was Rhodes Scholar ?	",
"	Who comprised the now-defunct comic book team known as the Champions ?	",
"	What crooner joined The Andrews Sisters for Pistol Packin Mama ?	",
"	What piano company claims its product is the `` Instrument of the immortals '' ?	",
"	What actress has received the most Oscar nominations ?	",
"	Who produces Spumante ?	",
"	Who earns their money the hard way ?	",
"	Who founded the People 's Temple Commune ?	",
"	What athlete makes the most money from sports merchandise sales ?	",
"	How many people in the world speak French ?	",
"	How many inches over six feet is the Venus de Milo ?	",
"	In which year was New Zealand excluded from the ANZUS alliance ?	",
"	When did CNN begin broadcasting ?	",
"	In what year did Thatcher become prime minister ?	",
"	How many months does it take the moon to revolve around the Earth ?	",
"	When did beethoven die ?	",
"	How much does a new railroad coal car cost ?	",
"	When did Mount St. Helen last have a significant eruption ?	",
"	When did World War I start ?	",
"	How many feet are there in a fathom ?	",
"	When was the battle of the Somme fought ?	",
"	How many people did Randy Craft kill ?	",
"	When did Spielberg direct `` Jaws '' ?	",
"	What is the size of the largest akita ?	",
"	What was Einstein 's IQ ?	",
"	What day was Pearl Harbor attacked in 1942 ?	",
"	What is the normal resting heart rate of a healthy adult ?	",
"	What is the population of Ohio ?	",
"	How many calories are there in a Big Mac ?	",
"	What year did Jack Nicklaus join the Professional Golfers Association tour ?	",
"	How many sonnets did Shakespeare write ?	",
"	What is the speed of the Mississippi River ?	",
"	How many Beatles ' records went #1 ?	",
"	What time of day did Emperor Hirohito die ?	",
"	How many years did it take James Joyce to write Ulysses ?	",
"	When was the women 's suffrage amendment ratified ?	",
"	What year did Hitler die ?	",
"	How much money are Dumbo 's ears insured for ?	",
"	What crooner joined The Andrews Sisters for Pistol Packin Mama ?	",
"	What piano company claims its product is the `` Instrument of the immortals '' ?	",
"	What actress has received the most Oscar nominations ?	",
"	Who produces Spumante ?	",
"	Who earns their money the hard way ?	",
"	Who founded the People 's Temple Commune ?	",
"	What athlete makes the most money from sports merchandise sales ?	",
"	Who discovered electricity ?	"]

for ask in testQuestion:
    processedTestQuestion = processQuestion(ask)
    print NBClassifier.classify(extract_features(getFeatureVector(processedTestQuestion, stopWords)))


