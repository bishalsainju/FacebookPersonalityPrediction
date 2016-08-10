#import regex
import re
import csv
import random
import json
import enchant
import nltk
from nltk import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.metrics import edit_distance

port = PorterStemmer()
Dictionary = enchant.Dict("en_US")
max_dist = 2

#start process_status
def processStatus(status):
        status = status.lower()
        status = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL', status)
        status = re.sub('@[^\s]+', 'AT_USER', status)
        status = re.sub('[\s]+', ' ', status)
        status = status.strip('\'"')
        return status
#end

#initialize stopWords
stopWords = []

#start replaceTwoOrMore
def replaceTwoOrMore(s):
        #look for 2 or more repetitions of character and replace with the character itself
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", s)
#end

#spellChecker
# def replace(words):
#     a = []
#     for word in words:
#         suggestions = Dictionary.suggest(word)
#         if suggestions and edit_distance(word, suggestions[0]) <= max_dist:
#             a.append(suggestions[0])
#         else:
#             a.append(word)
#     return a

#start getStopWordList
def getStopWordList(stopWordListFileName):
        #read the stopwords file and build a list
        stopWords = []
        stopWords.append('AT_USER')
        stopWords.append('URL')

        fp = open(stopWordListFileName, 'r')
        line = fp.readline()
        while line:
                word = line.strip()
                stopWords.append(word)
                line = fp.readline()
        fp.close()
        return stopWords
#end

#KNN
def distance(a, b):
    s = 0
    for i in range(len(a)):
        s += (a[i] - b[i]) ** 2
    return s

st = open('stopwords.txt', 'r')
stopWords = getStopWordList('stopwords.txt')

#start getfeatureVector
def getFeatureVector(status):
        featureVector = {}
        # stemmedFeatures = {}
        #split status into words
        postag = nltk.pos_tag(status.split())

        words = [x[0] for x in postag if x[1] not in ["NN", "IN", "CC", "TO", "NNS", "NNP", "NNPS"]]
        for w in words:
                # print w
                # suggestions = Dictionary.suggest(w)
                # print suggestions
                # if suggestions and edit_distance(w, suggestions[0]) <= max_dist:
                #     w = suggestions[0]
                    # print w
                #replace two or more with two ocurrences
                w = replaceTwoOrMore(w)
                #strip punctuation
                w = w.strip('\'"?,.')
                #check if the word starts with an alphabet
                val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
                #ignore if it is a stop word
                if(w in stopWords or val is None):
                        continue
                # suggestions = Dictionary.suggest(w)
                # if suggestions and edit_distance(w, suggestions[0]) <= max_dist:
                #     w = suggestions[0]
                if(Dictionary.check(w) == False):
                        continue
                else:
                        w = w.lower()
                        w = port.stem(w).encode('ascii')
                        if(w in stopWords):
                                continue
                        if w in featureVector: featureVector[w] += 1
                        else: featureVector[w] = 1
                # break
        return featureVector
#end

#Read the status one by one and process it

inpStatus = csv.reader(open('with_all.csv','r'), delimiter = ',', quotechar='"')
opStatus = csv.writer(open('concatenated.csv', 'w'), delimiter = ',', quotechar = '"')
#This consists of one status update of maybe the same or different user
statuses = []

#This consist of all the statuses of the particular userid
usermap = {}

#output label of the class of a particular user
userOpn = {}
userCon = {}
userExt = {}
userAgr = {}
userNeu = {}

#This contains the total bag of words, and making it set makes it unique
totalbagofwords = set()

#This is to get rid of the first row in the csv file which is the header file
for row in inpStatus:
    break

#This means to take only 200 users among the 250 users
TAKE = 200
cnt = 0 #to check whether the count reaches to 200

#Take each row in with_all csv file
for row in inpStatus:
    userid = row[0]
    status = row[1]
    ext = row[2]
    neu = row[3]
    agr = row[4]
    con = row[5]
    opn = row[6]
    cnt += userid not in usermap
    if cnt > TAKE:
        break
    processedStatus = processStatus(status)
    featureVector = getFeatureVector(processedStatus)
    if userid not in usermap:
        usermap[userid] = {}
        opStatus.writerow([str(userid), str(opn), str(con), str(ext), str(agr), str(neu)])
    for word in featureVector:
        totalbagofwords.add(word)
        count = featureVector[word]
        if word in usermap[userid]:
            usermap[userid][word] += count
        else:
            usermap[userid][word] = count
    userOpn[userid] = int(float(opn))
    userCon[userid] = int(float(con))
    userExt[userid] = int(float(ext))
    # print str(userid) + ":" + str(cnt) + ": " + str(userExt[userid])
    userAgr[userid] = int(float(agr))
    userNeu[userid] = int(float(neu))

writebow = json.dumps(usermap, indent=4)
open("bow.json", 'w').write(writebow)

# for id in usermap:
#     print(id, usermap[id])
#     print "Count: " + str(len(usermap[id]))
#     print("\n")

totalbagofwords = list(totalbagofwords)
totalbagofwords.sort()
# print replace(totalbagofwords)
# print "\nTotal No. of unique words: " + str(len(totalbagofwords)) + "\n"
writetbow= json.dumps(totalbagofwords, indent=4)
open("tbow.json", 'w').write(writetbow)

#total word count of the words in total bow
totalbow = {}
for word in totalbagofwords:
    totalbow[word] = 0

f = open('bowcount.txt', 'a')
for word in totalbagofwords:
    f.write(str(word)+":")
    for i in usermap:
        if word in usermap[i]:
            totalbow[word] += usermap[i][word]
    f.write(str(totalbow[word]))
    f.write("\n")
    # print str(word) + ": " + str(totalbow[word])

#featureset

bagcount = {}
training_feature_set = []
test_set = []
test_users = set()

for row in inpStatus:
        userid = row[0]
        test_users.add(userid)
        status = row[1]
        ext = row[2]
        neu = row[3]
        agr = row[4]
        con = row[5]
        opn = row[6]
        processedStatus = processStatus(status)
        featureVector = getFeatureVector(processedStatus)

        if userid not in usermap:
                usermap[userid] = {}
        for word in featureVector:
            if word not in bagcount: bagcount[word] = 0
            bagcount[word] += 1
            count = featureVector[word]
            if word in usermap[userid]: usermap[userid][word] += count
            else: usermap[userid][word] = count
        userOpn[userid] = int(float(opn))
        userCon[userid] = int(float(con))
        userExt[userid] = int(float(ext))
        userAgr[userid] = int(float(agr))
        userNeu[userid] = int(float(neu))

        #statuses.append((featureVector, ext, neu, agr, con, opn))
# listj = []
maxcount = {}
for i in usermap:
    for j in usermap[i]:
        if j not in maxcount:
            # listj.append(j)
            maxcount[j] = 0
        maxcount[j] = max(maxcount[j], usermap[i][j])

# print maxcount
# listj.sort()
# print listj, len(listj)

# amn= []
# for i in maxcount:
#     # print i
#     amn.append(str(i))
# amn.sort()
# print amn

writemc = json.dumps(maxcount, indent=4)
open("maxcount.json", 'w').write(writemc)

for i in usermap:
    data = usermap[i]
    # print data
    feature = [.5 + .5 * data[j] / (0 if j not in maxcount else maxcount[j])  if j in data else 0 for j in totalbagofwords]
    # print j
    if i in test_users:
        test_set.append([i, feature, userOpn[i], userCon[i], userExt[i], userAgr[i], userNeu[i]])
    else:
        training_feature_set.append([i, feature, userOpn[i], userCon[i], userExt[i], userAgr[i], userNeu[i]])

# writetfsbow = json.dumps(training_feature_set, indent=4)
# open("training_feature_set.json", 'w').write(writetfsbow)
# print(training_feature_set)
#
# writettsbow = json.dumps(test_set, indent=4)
# open("test_set.json", 'w').write(writettsbow)

#**********writing the feature vector in file******************
fo1 = open("testFeature.txt","w+")
for i1, i2, j1, j2, j3, j4, j5 in test_set:
    fo1.write("[")
    fo1.write("%s " %i1)
    ct = 0
    for k in i2:
        fo1.write(" %s:%s " %(totalbagofwords[ct], k))
        ct = ct +1
    fo1.write(": opn:%s con:%s ext:%s agr:%s neu:%s " %(j1, j2, j3, j4, j5))
    fo1.write("]\n")
fo1.close()

fo2 = open("trainingFeature.txt","w+")
for i1, i2, j1, j2, j3, j4, j5 in training_feature_set:
    fo2.write("[")
    fo2.write("%s " %i1)
    ct = 0
    for k in i2:
        fo2.write(" %s:%s " %(totalbagofwords[ct], k))
        ct = ct + 1
    fo2.write(": opn:%s con:%s ext:%s agr:%s neu:%s " %(j1, j2, j3, j4, j5))
    fo2.write("]\n")
fo2.close()
#end

misclassified = 0

for N in range(1, 1):
    misclassified = 0
    for feature, cls in test_set:
        dist = [1e15] * N
        classification = [0] * N
        for f2, cls2 in training_feature_set:
            dn = distance(feature, f2)
            for j in range(N):
                if dn < dist[j]:
                    dist[j] = dn
                    classification[j] = cls2
                    break
        final = sum(classification) / N
        # print 'original class ' + str(cls) + ' classified as ' + str(final)
        misclassified += cls != final
    print 'No of clusters in KNN:' + str(N) + ' Misclassified-Test-Set:' + str(misclassified) + ' Accuracy:' + str(1 - misclassified / 50.0)
#end loop
