'''
Setup for a chemical structure/log p analysis.
'''
import numpy as np, pandas as pd
from keras.models import Model
from keras.layers import Input, Dense, Conv1D, Flatten, BatchNormalization
from keras.layers import Embedding, SimpleRNN, GRU, LSTM, Bidirectional
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import keras.backend as K

class Categorizer:
    def __init__(self):
        self.map = {}

    def fit(self, iterable):
        for string in iterable:
            for ch in string:    
                if ch not in self.map:
                    self.map[ch] = len(self.map)
    
    def to_array(self, string):
        result = []
        for ch in string:
            if ch in self.map:
                result.append(self.map[ch])
            else:
                result.append(len(self.map))
        return np.array(result)

    def build(self, strlist):
        return np.array([self.to_array(string) for string in strlist])

class ChemModel:
    def __init__(self):
        self.categorizer = Categorizer()
        self.input = None
        self.output = None

    def add(self, layer):
        if self.input is None:
            self.input = Input(shape = layer.batch_input_shape[1:])
        if self.output is None:
            self.output = layer(self.input)
        else:
            self.output = layer(self.output)

    def fit(self, X, y, optimizer = 'adam', loss = 'binary_crossentropy', metrics = [], **kwargs):
        self.categorizer.fit(X)
        X = self.categorizer.build(X)
        self.model = Model(self.input, self.output)
        self.model.compile(optimizer = optimizer, loss = loss, metrics = metrics)
        self.model.fit(X, y, **kwargs)

    def predict(self, X, **kwargs):
        X = self.categorizer.build(X)
        return self.model.predict(X, **kwargs)

    def evaluate(self, X, y, **kwargs):
        X = self.categorizer.build(X)
        return self.model.evaluate(X, y, **kwargs)

def format_strings(strings):
    return [string[:50].ljust(50, '_') for string in strings]

def construct_ChemModel(vocab_size):
    model = ChemModel()
    model.add(Embedding(vocab_size, 5, input_length=50))
    #model.add(Bidirectional(GRU(64, activation = 'sigmoid')))
    model.add(Bidirectional(LSTM(128)))
    #model.add(SimpleRNN(64, activation = 'sigmoid'))
    #model.add(Flatten())
    model.add(Dense(64))
    model.add(Dense(32, activation = 'relu'))
    #model.add(Dense(16))
    model.add(Dense(1, activation = 'relu'))
    return model

def construct_conv_ChemModel(vocab_size):
    model = ChemModel()
    model.add(Embedding(vocab_size, 5, input_length=50))
    model.add(Conv1D(32, 3, activation = 'sigmoid'))
    #model.add(BatchNormalization())
    model.add(Flatten())
    #model.add(Dense(16))
    model.add(Dense(1, activation = 'relu'))
    return model

def r2_keras(y_true, y_pred):
    SS_res =  K.sum(K.square(y_true - y_pred))
    SS_tot = K.sum(K.square(y_true - K.mean(y_true))) 
    return (1 - SS_res/(SS_tot + K.epsilon()))

#==================================================================================
def main():
    df = pd.read_csv('logP_dataset.csv', header = None, names = ['chemical', 'logp'])
    X = format_strings(df['chemical'])
    y = df['logp'].values
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y)
    metric = -1
    while metric < 0:
        model = construct_ChemModel(100)
        #model = construct_conv_ChemModel(100)
        model.fit(Xtrain, ytrain, optimizer = Adam(lr = 0.0001), loss = 'mse', metrics=[r2_keras], epochs = 10)
        model.model.summary()
        metric = r2_score(ytest, model.predict(Xtest))
    print(metric)

if __name__ == '__main__':
    main()