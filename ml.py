import numpy as np 
from sklearn import linear_model, datasets
import csv

with open("x.csv", 'rb') as x_file: 
	reader = csv.reader(x_file, delimiter=' ')
	X_train = []
	for row in reader: 
		temp = row[0].split(',')
		temp[5] = float(temp[5])
		for i in range(len(temp)):
			temp[i] = int(temp[i])
		X_train.append(temp)


with open("y.csv", 'rb') as y_file: 
	reader = csv.reader(y_file, delimiter=' ')
	Y_train_pre = [] 
	for row in reader: 
		Y_train_pre.append(int(row[0]))

Y_train = []
Y_train.append(Y_train_pre) 
Y_train = np.array(Y_train).reshape((-1,1))


logreg = linear_model.LogisticRegression(C=1e5)

logreg.fit(X_train, Y_train.ravel())


X = ([[20, 20000, 20000, 3, 1000, 500, 0, 0]])
result = logreg.predict(X)
print result
