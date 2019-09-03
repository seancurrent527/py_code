'''
Set up for self-taught basic neural networking.
'''

import numpy as np
from grad_descent import *

class Unit:
    def __init__(self, size):
        self.params = np.random.rand(size + 1).astype('object') #initialize params as random values between 0 and 1
        self.input = np.zeros(size)
        self.out = 0

    def traverse(self, array):
        self.input = array
        assert len(array) == len(self.params) - 1
        output = self.params[-1] + sum(array * self.params[:-1])
        self.output = 0 if output < 0 else output
        return self.output

    def learn(self, gradient, lr = 0.1):
        self.params -= lr * gradient

class Layer:
    def __init__(self, input_size, units):
        self.units = [Unit(input_size) for i in range(units)]
        self.input = np.zeros(input_size)
        self.output = np.zeros(units)

    def traverse(self, array):
        self.input = array
        self.output = np.array([unit.traverse(array) for unit in self.units])
        return self.output

    def __getitem__(self, n):
        return self.units[n]

    def __len__(self):
        return len(self.units)

class Network:
    def __init__(self, input_size, output_size, layers):
        self.input_size = input_size
        self.output_size = output_size
        self.layers = []
        for i in range(len(layers)):
            if i == 0:
                self.layers.append(Layer(self.input_size, layers[i]))
            else:
                self.layers.append(Layer(layers[i-1], layers[i]))
        self.layers.append(Layer(layers[-1], self.output_size))

    def traverse(self, inputs):
        assert self.input_size == len(inputs)
        output = np.copy(inputs)
        for layer in self.layers:
            output = layer.traverse(output)
        return output

    def __getitem__(n):
        if type(n) is tuple:
            return self.layers[n[0]][n[1]]
        else:
            return self.layers[n]

    def __len__(self):
        return len(self.layers)

#=====================================================================================
def main():
    X = np.ones(784)
    net = Network(784, 10, (16,16))
    print(net.traverse(X))

if __name__ == '__main__':
    main()








