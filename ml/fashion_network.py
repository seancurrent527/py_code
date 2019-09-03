'''
fashion_network.py
Sean Current
'''

import scipy.io as sio, numpy as np, pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, Flatten, MaxPooling2D
from keras.utils import to_categorical
from keras.optimizers import Adadelta
import random, matplotlib.pyplot as plt

def get_data(): 
    #0 T-shirt/top 1 Trouser 2 Pullover 3 Dress 4 Coat 5 Sandal 6 Shirt 7 Sneaker 8 Bag 9 Ankle boot
    train = pd.read_csv('data\\fashion-mnist\\fashion-mnist_train.csv', delimiter = ',').values
    test = pd.read_csv('data\\fashion-mnist\\fashion-mnist_test.csv', delimiter = ',').values
    train_shuffle = np.random.permutation(len(train))
    test_shuffle = np.random.permutation(len(test))
    train, test = train[train_shuffle], test[test_shuffle]
    return train[:, 1:], train[:, 0], test[:, 1:], test[:, 0]

def format_labels(y):
    formatted = np.zeros((len(y), 10))
    for i in range(len(y)):
        formatted[i, y[i]] = 1
    return formatted

def create_network():
    model = Sequential()
    model.add(Dense(200, activation = 'sigmoid', input_shape = (784,)))
    #model.add(Dropout(0.1))
    model.add(Dense(100, activation = 'sigmoid'))
    #model.add(Dropout(0.1))
    model.add(Dense(10, activation = 'softmax'))
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

def compile_and_train(model, X, y):
    model.compile(optimizer = Adadelta(),#'rmsprop',
                  loss = 'categorical_crossentropy',
                  metrics = ['accuracy'])
    model.fit(X, y, epochs = 10, batch_size = 32)
    return model

def compile_and_train2(model, X, y):
    X = np.reshape(X, (len(X), 28, 28, 1))
    model.compile(optimizer = 'rmsprop',
                  loss = 'categorical_crossentropy',
                  metrics = ['accuracy'])
    model.fit(X, y, epochs = 3, batch_size = 32)
    return model

def view_predictions(X, y, model, num = 10):
    dat = {0: 'T-shirt/top', 1: 'Trouser',
           2: 'Pullover', 3: 'Dress',
           4: 'Coat', 5: 'Sandal',
           6: 'Shirt', 7: 'Sneaker',
           8: 'Bag', 9: 'Ankle boot'}
    for i in range(num):
        idx = random.randrange(0, len(X))
        vector, label = X[idx], y[idx]
        yhat = model.predict(np.array([vector]))
        print('Actual:', dat[label.argmax()])
        print('Predicted:', dat[yhat.argmax()])
        plt.matshow(np.reshape(vector, (28,28)), cmap = 'binary')
        plt.show()
    
def view_predictions2(X, y, model, num = 10):
    dat = {0: 'T-shirt/top', 1: 'Trouser',
           2: 'Pullover', 3: 'Dress',
           4: 'Coat', 5: 'Sandal',
           6: 'Shirt', 7: 'Sneaker',
           8: 'Bag', 9: 'Ankle boot'}
    for i in range(num):
        idx = random.randrange(0, len(X))
        vector, label = X[idx], y[idx]
        yhat = model.predict(np.array([vector]).reshape(1,28,28,1))
        print('Actual:', dat[label.argmax()])
        print('Predicted:', dat[yhat.argmax()])
        plt.matshow(np.reshape(vector, (28,28)), cmap = 'binary')
        plt.show()

#=========================================================================
def main():
    Xtrain, ytrain, Xtest, ytest = get_data()
    ytrain, ytest = format_labels(ytrain), format_labels(ytest)
    model = create_network2()
    compile_and_train2(model, Xtrain, ytrain)
    print(model.evaluate(Xtest.reshape(len(Xtest), 28, 28, 1), ytest, batch_size = 128))
    view_predictions2(Xtest, ytest, model)

if __name__ == '__main__':
    main()

