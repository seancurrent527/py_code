'''
mnist_network.py
Sean Current
'''

import scipy.io as sio, numpy as np, pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, Flatten, MaxPooling2D
from keras.utils import to_categorical
from keras.optimizers import Adadelta
import random, matplotlib.pyplot as plt

def get_data(): 
    mnist = sio.loadmat('mnist-original.mat') # not shuffled
    return mnist['data'].T, mnist['label'][0]

def preprocess(X, y):
    labels = to_categorical(y, num_classes = None)
    shuffle_index = np.random.permutation(len(X))
    X, labels = X[shuffle_index], labels[shuffle_index]
    return X[:60000], labels[:60000], X[60000:], labels[60000:]

def create_network():
    model = Sequential()
    model.add(Dense(150, activation = 'sigmoid', input_shape = (784,)))
    #model.add(Dropout(0.1))
    #model.add(Dense(16, activation = 'sigmoid'))
    #model.add(Dropout(0.1))
    model.add(Dense(10, activation = 'softmax'))
    return model

def compile_and_train(model, X, y):
    model.compile(optimizer = 'rmsprop',
                  loss = 'categorical_crossentropy',
                  metrics = ['accuracy'])
    model.fit(X, y, epochs = 10, batch_size = 32)
    return model

def create_network2():
    model = Sequential()
    #Kernel 3 is best
    model.add(Conv2D(32, kernel_size = 3, activation = 'relu', input_shape = (28,28,1)))
    model.add(MaxPooling2D(pool_size = (2,2)))
    model.add(Conv2D(32, kernel_size = 3, activation = 'relu'))
    #model.add(MaxPooling2D(pool_size = (2,2)))
    model.add(Flatten())
    model.add(Dense(128, activation = 'sigmoid'))
    model.add(Dense(10, activation = 'softmax'))
    return model

def compile_and_train2(model, X, y):
    X = np.reshape(X, (len(X), 28, 28, 1))
    model.compile(optimizer = 'rmsprop',
                  loss = 'categorical_crossentropy',
                  metrics = ['accuracy'])
    model.fit(X, y, epochs = 3, batch_size = 32)
    return model

def main():
    X, y = get_data()
    Xtrain, ytrain, Xtest, ytest = preprocess(X, y)
    model = create_network2()
    compile_and_train2(model, Xtrain, ytrain)
    print(model.evaluate(Xtest.reshape(len(Xtest), 28, 28, 1), ytest, batch_size = 128))

if __name__ == '__main__':
    main()

