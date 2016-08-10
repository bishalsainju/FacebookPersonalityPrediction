from ps import processStatus
from gfv import getFeatureVector
from sw  import compStopWords
from stem import stemm
from wcntr import cntr
import csv
import json

inpStatus = csv.reader(open('with_all.csv','r'), delimiter = ',', quotechar='"')

usermap = {}
userOpn = {}
userCon = {}
userExt = {}
userAgr = {}
userNeu = {}
totalbagofwords = set()

for row in inpStatus:
    break
for row in inpStatus:
    userid = row[0]
    status = row[1]
    ext = row[2]
    neu = row[3]
    agr = row[4]
    con = row[5]
    opn = row[6]
    processedStatus = processStatus(status)
    a1 = getFeatureVector(processedStatus)
    final1 = compStopWords(a1)
    final2 = stemm(final1)
    final3 = compStopWords(final2)
    featureVector = cntr(final3)
    if userid not in usermap:
        usermap[userid] = {}
    for word in featureVector:
        totalbagofwords.add(word)
        count = featureVector[word]
        if word in usermap[userid]:
            usermap[userid][word] += count
        else:
            usermap[userid][word] = count
    userOpn[userid] = round(float(opn))
    userCon[userid] = round(float(con))
    userExt[userid] = round(float(ext))
    userAgr[userid] = round(float(agr))
    userNeu[userid] = round(float(neu))

totalbagofwords = list(totalbagofwords)
totalbagofwords.sort()

# totalbow = {}
# for word in totalbagofwords:
#     totalbow[word] = 0
#
# opStatus = csv.writer(open('wordcountintbow.csv', 'w'), delimiter = ',', quotechar = '"')
# opStatus.writerow(["Word", "Count"])
#
# for word in totalbagofwords:
#     for i in usermap:
#         if word in usermap[i]:
#             totalbow[word] += usermap[i][word]
#     opStatus.writerow([word, int(str(totalbow[word]))])

# for id in usermap:
#     print(id, usermap[id])
#     print "Count: " + str(len(usermap[id]))
#     print("\n")

# print usermap
# totalbagofwords = list(totalbagofwords)
# totalbagofwords.sort()
# for word in totalbagofwords:
#     print word
# writebow = json.dumps(userNeu, indent=4)
# open("userNeu.json", 'w').write(writebow)
