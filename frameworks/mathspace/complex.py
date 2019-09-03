'''
Functions for Complex numbers.
'''

import math

class Complex:
    def __init__(self, real=0, imag=0):
        if type(real) == Complex:
            self._re = real._re
            self._im = real._im
        else:
            self._re = real
            self._im = imag
        
    def __str__(self):
        real, imag = round(self._re, 3), round(self._im, 3)
        if int(real) == real: real = int(real)
        if int(imag) == imag: imag = int(imag)
        if self._im == 0:
            return str(real)
        elif self._re == 0:
            return str(imag) + 'i'
        return str(real) + ' + ' + str(imag) + 'i'
        
    def __repr__(self):
        return str(self)    #'Complex(' + str(self._re) + ',' + str(self._im) + ')'

    def __eq__(self, other):
        if type(other) in (int, float): other = Complex(other, 0) 
        return self._re == other._re and self._im == other._im
        
    def __add__(self, other):
        if type(other) in (int, float): other = Complex(other, 0)
        return Complex(self._re + other._re, self._im + other._im)
        
    def __mul__(self, other):
        if type(other) in (int, float): other = Complex(other, 0)
        if type(other) == Complex:
            return Complex(self._re * other._re - self._im * other._im,\
                       self._im * other._re + self._re * other._im)
        else: return other * self
                       
    def __rmul__(self, other):
        return self * other
                       
    def __radd__(self, other):
        if type(other) in (int, float): other = Complex(other, 0)
        return Complex(self._re + other._re, self._im + other._im)
    
    def __neg__(self):
        return Complex(-self._re, -self._im)
        
    def __sub__(self, other):
        if type(other) in (int, float): other = Complex(other, 0)
        return Complex(self._re - other._re, self._im - other._im)
        
    def __abs__(self):
        return math.sqrt(self._re ** 2 + self._im ** 2)
        
    def conjugate(self):
        return Complex(self._re, -self._im)
        
    def __invert__(self):
        return Complex(self._re / abs(self) ** 2, -self._im / abs(self) ** 2)
        
    def __truediv__(self, other):
        if type(other) in (int, float): other = Complex(other, 0)
        return self * ~other
        
    def __rtruediv__(self, other):
        if type(other) in (int, float): other = Complex(other, 0)
        return other * ~self
    
    def __pow__(self, other):
        result = Complex(1)
        for i in range(other):
            result *= self
        return result
    
    def get_real(self):
        return self._re
        
    def get_imag(self):
        return self._im
        
    def __round__(self, n):
        self._re = round(self._re, n)
        self._im = round(self._im, n)
        
def sqrt(num):
    return math.sqrt(num) if num >= 0 else Complex(0, math.sqrt(-num))
    
    
    
    
    