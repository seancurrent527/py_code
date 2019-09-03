'''
Implementation for a gradient descent scanner.
Sean Current
'''

import numpy as np

class OrthoSet:
    def __init__(self, dimension = 2):
        len = lambda x: int(x) if type(x) in (int, float) else len(x)
        self.dimension = len(dimension)
        self.magnitude = 1
        
    def __str__(self):
        return '\n'.join(str(v) for v in self)
        
    def __getitem__(self, n):
        if n >= self.dimension:
            raise IndexError
        ortho = np.zeros(self.dimension)
        ortho[n] = self.magnitude
        return ortho
        
    def __iter__(self):
        self._iterator = 0
        return self
        
    def __next__(self):
        self._iterator += 1
        try:
            return self[self._iterator-1]
        except IndexError:
            self._iterator = 0
            raise StopIteration
        
    def __len__(self):
        return self._dimension
        
class Gradient:
    def __init__(self, point, func, args = [], tol = 0.000001):
        point = point.astype(np.float64)
        self.func = func
        self.args = args
        self.point = point
        self.value = self.func(self.point, *self.args)
        self.basis = OrthoSet(len(point))
        self.tol = tol
        self.grad = self.approx()
        
    def __str__(self):
        return str(self.grad)
        
    def approx(self):
        return np.array([(self.func(self.point + self.tol * bas, *self.args) - self.value)/self.tol for bas in self.basis])

    def __add__(self, other):
        return self.grad + other
        
    def __radd__(self, other):
        return other + self.grad
        
    def __mul__(self, other):
        return self.grad * other
        
    def __rmul__(self, other):
        return other * self.grad
        
    def __sub__(self, other):
        return self.grad - other
        
    def __rsub__(self, other):
        return other - self.grad
        
    def __neg__(self):
        return -self.grad
        
class LearningRate:
    def __init__(self, rate):
        self.rate = rate
        
    def search(self, point, grad, func, args = [], tol = 0.000001, nest = 5):
        curr = func(point, *args)
        next = curr; curr += 1
        for i in range(nest):
            while next < curr:
                curr = next
                point -= grad * self.rate
                next = func(point, *args)
                if abs(next - curr) < tol:
                    break
            if abs(next - curr) < tol:
                break
            self.rate /= 2            
        return point
            
def IntoTheUnknown(point, func, args = [], tol = 0.000001, lr = 0.1, nest = 5, num_iter = 100):
    point = point.astype(np.float64)
    for i in range(num_iter):
        grad = Gradient(point, func, args, tol = tol)
        point = LearningRate(lr).search(point, grad, func, args, nest = nest)
    return point
    
