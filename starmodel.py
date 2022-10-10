import numpy as np
from pickle import dump
from keras.layers import Dense
from keras.models import Sequential
from keras.layers import Dropout
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.models import model_from_json
import csv
from sklearn.externals import joblib

def getArray(fileName):
    f = open(fileName, "r")
    reader = csv.reader(f)
    next(f)
    data = [d for d in reader]
    f.close()

    for i, line in enumerate(data):
        for j, number in enumerate(line):
            #try:
                data[i][j] = float(number)
            #except:
                #data[i][j] = 0

    return data

# Importing the dataset
# x is right signals and left signals
#desna = getArray("ati2111/desna.067655.csv")
#leva = getArray("ati2111/leva.762117.csv")
desna = getArray("sara1501/desnaExtremeDropedAverage.csv")
leva = getArray("sara1501/levaExtremeDropedAverage.csv")
neutral = getArray("sara1501/neutralExtremeDropedAverage.csv")
X = desna + leva + neutral

y = np.empty([(len(desna)+len(leva)+len(neutral)), 3], dtype=int)
for i in range(len(desna)):
    y[i] = np.array([0, 0, 1])
for i in range(len(leva)):
    y[i + len(desna)] = np.array([1, 0, 0])
for i in range(len(neutral)):
    y[i + len(desna) + len(leva)] = np.array([0, 1, 0])


# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Feature Scaling
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
scFilename = 'modeli/scaler1601-sara1601.save'
joblib.dump(sc, scFilename)


# Initialising the ANN
model = Sequential()

model.add(Dropout(rate=0.2))

# Adding the input layer and the first hidden layer

model.add(Dense(32, activation = 'relu', input_dim = 5))


#model.add(Dense(32, activation = 'relu'))


model.add(Dense(units=3))

# model.add(Dense(1))
# Compiling the ANN
model.compile(optimizer='adam', loss='mean_squared_error')


# Fitting the ANN to the Training set
model.fit(X_train, y_train, batch_size=50, epochs=40)
y_pred = model.predict(X_test)
diff = 0
for i in range(0, len(y_test)):
    # print ("-------------------------------------------------------------------------------------------------------------")
    # print ("a:", y_test[i])
    # print ("p:", y_pred[i])
    # print ("-------------------------------------------------------------------------------------------------------------")
    diff = diff + abs(y_test[i][0]-round(y_pred[i][0])) + abs(y_test[i][0]-round(y_pred[i][0]))
print(diff)
print(1 - diff/len(y_test))


# model_json = model.to_json()
# with open("modeli/model1601-sara1601.json", "w") as json_file:
#     json_file.write(model_json)
# #serialize weights to HDF5
# model.save_weights("modeli/model1601-sara1601.h5")
# print("Saved model to disk")



# plt.plot(y_test, color='red', label='Real data')
# plt.plot(y_pred, color='blue', label='Predicted data')
# plt.title('Prediction')
# plt.legend()
# plt.show()

# serialize model to JSON


# later...

# # load json and create model
# json_file = open('model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# # load weights into new model
# loaded_model.load_weights("model.h5")
# print("Loaded model from disk")

# # evaluate loaded model on test data
# loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
# score = loaded_model.evaluate(X, Y, verbose=0)
# print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
