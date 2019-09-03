from keras.models import Sequential, Model
from keras.layers import Dense, Input, Lambda, Reshape, Conv2D, Flatten, BatchNormalization
import numpy as np
import keras.backend as K

class AutoEncoder:
    def __init__(self, data):
        self.data = data
        self.input = Input(shape = self.data.shape[1:])
        self.output = Lambda(lambda x: x)(self.input)

    def parse(self):
        model = Model(self.input, self.output)
        return model.predict(self.data)

    def add(self, layer, **kwargs):
        data = self.parse()
        x = Input(data[0].shape)
        l = layer(x)
        if len(K.int_shape(l)) > 2: l = Flatten()(x)
        l = Dense(np.prod(data[0].shape))(x)
        l = Reshape(data[0].shape)(x)
        mod = Model(x, l)
        mod.compile(optimizer = 'adam', loss ='mean_squared_error')
        mod.fit(data, data, **kwargs)
        self.output = layer(self.output)

    def fit(self, X, y, layer, loss = 'binary_crossentropy', metrics = [], **kwargs):
        self.output = layer(self.output)
        self.model = Model(self.input, self.output)
        self.model.compile(optimizer = 'adam', loss = loss, metrics=metrics)
        self.model.fit(X, y, **kwargs)

    def predict(self, X, **kwargs):
        return self.model.predict(X, **kwargs)

    def evaluate(self, X, y, **kwargs):
        return self.model.evaluate(X, y, **kwargs)

def test():
    X=np.random.rand(100, 28, 28, 1)
    y = np.random.rand(100)
    m = AutoEncoder(X)
    m.add(Conv2D(2, kernel_size = 3, input_shape = (28,28,1), data_format='channels_last'))
    m.add(Flatten())
    m.fit(X, y, Dense(1), loss='mse')

    X=np.random.rand(100, 784)
    y = np.random.rand(100)
    m = AutoEncoder(X)
    m.add(Dense(32))
    m.fit(X, y, Dense(1), loss='mse')

if __name__ == '__main__':
    test()