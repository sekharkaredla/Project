from sklearn import tree
import numpy as np
import random

data_violent = range(1,130)
data_nonviolent = range(1,130)


X_train = []
Y_train = []

X_test = []
Y_test = []

m = 0
l = 0

for i in data_nonviolent:
    try:
        file_name = 'violent_features_NON_VIOLENT/nonvio_'+str(i)+'.txt'
        file_obj = open(file_name,'r')
        vif = np.loadtxt(file_obj)
        if vif.shape[0] == 336:# avoiding hd videos
            continue
        l += 1
        X_train.append(vif)
        Y_train.append(0)
        file_obj.close()
    except:
        continue
for i in data_violent:
    try:
        file_name = 'violent_features_VIOLENT/vio_'+str(i)+'.txt'
        file_obj = open(file_name,'r')
        vif = np.loadtxt(file_obj)
        if vif.shape[0] == 336:# avoiding hd videos
            continue
        m += 1
        X_train.append(vif)
        Y_train.append(1)
        file_obj.close()
    except:
        continue
for i in data_nonviolent:
    try:
        file_name = 'violent_features_NON_VIOLENT/nonvio_'+str(i)+'.txt'
        file_obj = open(file_name,'r')
        vif = np.loadtxt(file_obj)
        if vif.shape[0] == 336:# avoiding hd videos
            continue
        X_test.append(vif)
        Y_test.append(0)
        file_obj.close()
    except:
        continue
for i in data_violent:
    try:
        file_name = 'violent_features_VIOLENT/vio_'+str(i)+'.txt'
        file_obj = open(file_name,'r')
        vif = np.loadtxt(file_obj)
        if vif.shape[0] == 336:# avoiding hd videos
            continue
        X_test.append(vif)
        Y_test.append(1)
        file_obj.close()
    except:
        continue

print l,m
# initial weights done
i = 0
weights = []
for i in range(0,len(Y_train)):
    if Y_train[i] == 1:
        weights.append(1.0/(2*m))
    else:
        weights.append(1.0/(2*l))

for t in range(0,5):
    # normalize weights
    weights = [x/sum(weights) for x in weights]

    # generate classifier for each feature
    classifiers = {}
    for each_feature in range(0,252):
        train_data_X = []
        train_data_Y = []
        i = 0
        for each_set in X_train:
            train_data_X.append(each_set[each_feature])
            train_data_Y.append(Y_train[i])
            i += 1
        clf = tree.DecisionTreeClassifier(max_depth = 1)
        clf.fit(np.array(train_data_X).reshape(-1,1),np.array(train_data_Y).reshape(-1,1))
        classifiers[each_feature] = clf

    # calculate error for all classifiers
    errors = [0.0] * 252
    for each_feature in range(0,252):
        clf = classifiers[each_feature]
        i = 0
        preds = []
        for each_set in X_test:
			test_data_X = each_set[each_feature]
			i += 1
			preds.append(clf.predict(test_data_X.reshape(1,-1))[0])
        i = 0

        for each_pred in preds:
            errors[each_feature] += weights[i] * abs(each_pred - Y_test[i])
            i += 1

    print errors
    min_error_classifier_index = np.where(errors == np.amin(errors))

    min_error_classifier_index = min_error_classifier_index[0][0]

    beta_change = errors[min_error_classifier_index]/(1.0 - errors[min_error_classifier_index])

    classifier = classifiers[min_error_classifier_index]

    classifier_preds = []

    for each_set in X_test:
        classifier_preds.append(classifier.predict(each_set[min_error_classifier_index].reshape(1,-1))[0])

    i = 0
    for each_pred in classifier_preds:
        weights[i] = weights[i] * (beta_change ** (abs(each_pred - Y_test[i])))

    # print weights
    print '----------------------------------------------'
