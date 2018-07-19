import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import csv

import time
import datetime

EPOCHS = 500
SAVING_STEP = 10

# load dataset
dataset = np.loadtxt("dataset_15_20-50.csv", delimiter=',')
# split into X and Y
n_inputs  = 4
n_outputs = 2
X = dataset[:,0:n_inputs]
Y = dataset[:,n_inputs:]
# split into train and test
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)



model = Sequential()

layer_sizes = [128, 64, 36, 16 ,8]
layer_activations = ['relu', 'relu','relu', 'relu', 'relu']

for i, l in enumerate(layer_sizes):
    if i == 0:
        model.add(Dense(l, activation=layer_activations[i], input_shape=(n_inputs,)))
    else:
        model.add(Dense(l, activation=layer_activations[i]))

model.add(Dense(n_outputs, activation='sigmoid'))

model.summary()
model.compile(loss='mean_squared_error', optimizer='adam') #, metrics=['mae', euclid_dist])


loss = []
val_loss = []


ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
csvreport = open('nets/{}.csv'.format(st), 'wb')
csvwriter = csv.writer(csvreport)
for epoch in range(EPOCHS):
    history = model.fit(x_train, y_train,
        batch_size=64,
        epochs=1,
        # validation_split=0.2,
        verbose=1,
        validation_data=(x_test,y_test)
    )

    loss += history.history['loss']
    val_loss += history.history['val_loss']

    print "Epoch: {} - loss: {} - val_loss: {}".format(epoch, loss[-1], val_loss[-1])

    if epoch % SAVING_STEP == 0:
        print "saving model with", epoch, "epochs"
        model.save('nets/model{}.h5'.format(st))
        csvwriter.writerow([loss, val_loss])
        plt.figure(figsize=(5,5))
        plt.plot(np.arange(1, len(loss)+1), loss)
        plt.plot(np.arange(1, len(val_loss)+1), val_loss)
        # plt.show()
        image_path = "nets/trained{}.png".format(st)
        plt.savefig(image_path)

print "saving final model with", epoch, "epochs"
model.save('nets/model{}.h5'.format(st))

plt.figure(figsize=(8,8))
plt.plot(np.arange(1, len(loss)+1), loss)
plt.plot(np.arange(1, len(val_loss)+1), val_loss)
# plt.show()
image_path = "nets/trained{}.png".format(st)
plt.savefig(image_path)