'''
Class setup for vectors.
'''

from complex import *
from matrix import *

class Vector:
    def __init__(self, vec = ()):
        self._vec = [Complex(v) for v in vec]
        self._dim = len(self._vec)
        
    def __str__(self):
        return str(self._vec)
        
    def __repr__(self):
        return str(self)    #'Vector(' + str(self) + ')'
        
    def __add__(self, other):
        assert self._dim == other._dim, 'ERROR: Vectors must have the same dimension'
        result = [self._vec[i] + other._vec[i] for i in range(self._dim)]
        return Vector(result)
        
    def __neg__(self):
        return Vector([-x for x in self._vec])
        
    def __sub__(self, other):
        return self + (-other)
        
    def new_scale(self, n):
        return Vector([x * n for x in self._vec])
    
    def scale(self, n):
        self._vec = [x * n for x in self._vec]
        
    def __mul__(self, other):
        if type(other) not in (Vector, Matrix):
            return Vector([v * other for v in self._vec])
        if type(other) == Vector:
            assert self._dim == other._dim, 'ERROR: Vectors must have the same dimension'
            return sum([self._vec[i] * other._vec[i] for i in range(self._dim)])
        if type(other) == Matrix:
            raise ValueError("Vectors can only be multiplied by Matrices on the left.")
    
    def __rmul__(self, other):
        if type(other) == Matrix:
            return Vector([other.row(i) * self for i in range(other._cdim)])
        return self * other
    
    def __truediv__(self, other):
        return self * (1/other)
        
    def __len__(self):
        return self._dim
        
    def conjugate(self):
        return Vector([num.conjugate() for num in self._vec])
        
    def __round__(self, n):
        self._vec = [round(v, n) for v in self._vec]
        
    def __getitem__(self, n):
        return self._vec[n]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    