'''
mnist_network.py
Sean Current
'''

import scipy.io as sio, numpy as np, pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, Flatten, MaxPooling2D, Layer
from keras.utils import to_categorical
from keras.optimizers import Adadelta
import random, matplotlib.pyplot as plt
from keras import initializers, regularizers, constraints, activations
import keras.backend as K


class ConCurrent(Layer):
    def __init__(self, units, repeats,
                 activation=None,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 **kwargs):
        if 'input_shape' not in kwargs and 'input_dim' in kwargs:
            kwargs['input_shape'] = (kwargs.pop('input_dim'),)
        super(ConCurrent, self).__init__(**kwargs)
        assert type(units) in (int, list), "units must be a list or integer"
        if type(units) is int:
            assert repeats is not None, "if units is an integer, repeats must be specified"
            self.units = [units for _ in range(repeats)]
        else:
            self.units = units
        self.repeats = len(self.units)
        self.activation = activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = initializers.get(kernel_initializer)
        self.bias_initializer = initializers.get(bias_initializer)
        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.bias_regularizer = regularizers.get(bias_regularizer)
        self.activity_regularizer = regularizers.get(activity_regularizer)
        self.kernel_constraint = constraints.get(kernel_constraint)
        self.bias_constraint = constraints.get(bias_constraint)

    def build(self, input_shape):
        assert len(input_shape) >= 2
        self.kernels = []
        self.biases = []
        in_units = input_shape[-1]
        for i, out_units in enumerate(self.units):
            self.kernels.append(self.add_weight(name = 'kernel_' + str(i),
                                    shape = (in_units, out_units),
                                    initializer = self.kernel_initializer,
                                    regularizer = self.kernel_regularizer,
                                    constraint = self.kernel_constraint,
                                    trainable = True))
            if self.use_bias:
                self.biases.append(self.add_weight(name = 'bias_' + str(i),
                                    shape = (out_units,),
                                    initializer = self.bias_initializer,
                                    regularizer = self.bias_regularizer,
                                    constraint = self.bias_constraint,
                                    trainable = True))
            in_units = in_units + out_units
        super(ConCurrent, self).build(input_shape)

    def call(self, inputs):
        for i, kernel in enumerate(self.kernels):
            output = K.dot(inputs, kernel)
            if self.use_bias:
                output = K.bias_add(output, self.biases[i], data_format='channels_last')
            if self.activation is not None:
                output = self.activation(output)
            inputs = K.concatenate([inputs, output])
        return inputs

    def compute_output_shape(self, input_shape):
        assert input_shape and len(input_shape) >= 2
        assert input_shape[-1]
        output_shape = list(input_shape)
        output_shape[-1] = sum(self.units) + input_shape[-1]
        return tuple(output_shape)

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
    model.fit(X, y, epochs = 100, batch_size = 32)
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

def create_network3():
    model = Sequential()
    model.add(ConCurrent(32, 4, activation = 'relu', input_shape = (784,)))
    model.add(Dense(10, activation='softmax'))
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
    model = create_network3()
    compile_and_train(model, Xtrain, ytrain)
    print(model.evaluate(Xtest, ytest, batch_size = 128))

if __name__ == '__main__':
    main()

