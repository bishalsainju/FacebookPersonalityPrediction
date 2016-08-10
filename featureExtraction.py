import json
import csv

def featExtr():
    with open('analysisFiles/usermap.json') as json_data:
        usermap = json.load(json_data)
    with open('analysisFiles/userOpn.json') as json_data1:
        userOpn = json.load(json_data1)
    with open('analysisFiles/userCon.json') as json_data2:
        userCon = json.load(json_data2)
    with open('analysisFiles/userExt.json') as json_data3:
        userExt = json.load(json_data3)
    with open('analysisFiles/userAgr.json') as json_data4:
        userAgr = json.load(json_data4)
    with open('analysisFiles/userNeu.json') as json_data5:
        userNeu = json.load(json_data5)

    f = open("analysisFiles/totalBOW.txt", "r")
    lines = f.read().split('\n')
    lines = lines[1:-1]
    f.close()

    totalbagofwords = set()
    totalbagofwords = list(lines)
    totalbagofwords.sort()

    training_feature_set = []
    test_set = []
    training_users = set()

    TAKE = 200
    cnt = 0

    for id in usermap:
        training_users.add(id)
        cnt += 1
        if cnt >= TAKE:
            break

    maxcount = {}
    for i in usermap:
        for j in usermap[i]:
            if j not in maxcount:
                # listj.append(j)
                maxcount[j] = 0
            maxcount[j] = max(maxcount[j], usermap[i][j])

    for i in usermap:
        data = usermap[i]
        feature = [.5 + .5 * data[j] / (0 if j not in maxcount else maxcount[j])  if j in data else 0 for j in totalbagofwords]
        if i not in training_users:
            test_set.append([i, feature, userOpn[i], userCon[i], userExt[i], userAgr[i], userNeu[i]])
        else:
            training_feature_set.append([i, feature, userOpn[i], userCon[i], userExt[i], userAgr[i], userNeu[i]])

    data_set = []
    data_set.append(training_feature_set)
    data_set.append(test_set)
    return data_set
