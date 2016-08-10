from featureExtraction import featExtr
aList = []
aList = featExtr()
training_feature_set = []
test_set = []
training_feature_set = aList[0]
test_set = aList[1]
#KNN
def distance(a, b):
    s = 0
    for i in range(len(a)):
        s += (a[i] - b[i]) ** 2
    return s

misclassified = 0
matrix = [[0 for i in range(5)] for j in xrange(5)]
for N in range(1, 2):
    misclassified = 0
    for id, feature, o, c, e, a, n in test_set:
        dist = [1e15] * N
        classification = [0] * N
        for id2, f2, o1, c1, e1, a1, n1 in training_feature_set:
            dn = distance(feature, f2)
            for j in range(N):
                if dn < dist[j]:
                    dist[j] = dn
                    classification[j] = o1
                    break
        final = sum(classification) / N
        # print 'original class ' + str(o) + ' classified as ' + str(final)
        if o == 1:
            if final == 1:
                matrix[0][0] += 1
            elif final == 2:
                matrix[0][1] += 1
            elif final == 3:
                matrix[0][2] += 1
            elif final == 4:
                matrix[0][3] += 1
            elif final == 5:
                matrix[0][4] += 1
        elif o == 2:
            if final == 1:
                matrix[1][0] += 1
            elif final == 2:
                matrix[1][1] += 1
            elif final == 3:
                matrix[1][2] += 1
            elif final == 4:
                matrix[1][3] += 1
            elif final == 5:
                matrix[1][4] += 1
        elif o == 3:
            if final == 1:
                matrix[2][0] += 1
            elif final == 2:
                matrix[2][1] += 1
            elif final == 3:
                matrix[2][2] += 1
            elif final == 4:
                matrix[2][3] += 1
            elif final == 5:
                matrix[2][4] += 1
        elif o == 2:
            if final == 1:
                matrix[3][0] += 1
            elif final == 2:
                matrix[3][1] += 1
            elif final == 3:
                matrix[3][2] += 1
            elif final == 4:
                matrix[3][3] += 1
            elif final == 5:
                matrix[3][4] += 1
        elif o == 4:
            if final == 1:
                matrix[4][0] += 1
            elif final == 2:
                matrix[4][1] += 1
            elif final == 3:
                matrix[4][2] += 1
            elif final == 4:
                matrix[4][3] += 1
            elif final == 5:
                matrix[4][4] += 1
print "The Cross Validation Matrix is:"
for a in matrix:
    print a
