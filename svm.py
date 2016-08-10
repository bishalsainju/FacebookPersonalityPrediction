from sklearn import svm
from sklearn.decomposition import TruncatedSVD
from featureExtraction import featExtr

aList = []
aList = featExtr()
training_feature_set = []
test_set = []
training_feature_set = aList[0]
test_set = aList[1]

for a in range(1,50):
    svd = TruncatedSVD(n_components = a)

    xTrain = [row[1] for row in training_feature_set]
    x = svd.fit_transform(xTrain)
    y = [row[6] for row in training_feature_set]
    clf = svm.SVC(kernel = 'linear', C=1).fit(x, y)


    xTest  = [row[1] for row in test_set]
    xT = svd.fit_transform(xTest)
    yT = [row[6] for row in test_set]

    # pred = clf.predict(xT)

    # for i, j in enumerate(pred):
    #     print(j, 'actual', yT[i])

    s= clf.score(xT, yT)
    print(str(a) + ": " + str(s))
