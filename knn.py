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

for N in range(1, 100):
    misclassified = 0
    for id, feature, o, c, e, a, n in test_set:
        # print feature
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
        # print 'original class ' + str(cls) + ' classified as ' + str(final)
        misclassified += o != final
    print 'No of clusters in KNN:' + str(N) + ' Misclassified-Test-Set:' + str(misclassified) + ' Accuracy:' + str(1 - misclassified / 50.0)
#end loop
