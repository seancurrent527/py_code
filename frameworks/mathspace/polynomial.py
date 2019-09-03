'''
Polynomial class setup.
'''

import math

class Polynomial:
    def __init__(self, coefficients):
        self._terms = {i: coefficients[i] for i in range(len(coefficients))}
        self._coefs = [self._terms[x] for x in sorted(self._terms.keys())]
        self._deg = len(self._terms) - 1
        
    def __repr__(self):
        return 'Polynomial(' + str(self._coefs) + ')'
        
    def __str__(self):
        return ' + '.join(str(self._terms[i]) + 'x^' + str(i)\
        for i in sorted(self._terms.keys()))
        
    def __eq__(self, other):
        if type(other) != Polynomial:
            other = Polynomial([other])
        return self._terms == other._terms
    
    def __add__(self, other):
        if type(other) != Polynomial:
            other = Polynomial([other])
        result = self._terms.copy()
        for key in other._terms:
            if key in result:
                result[key] += other._terms[key]
            else:
                result[key] = other._terms[key]
        return Polynomial([result[i] for i in sorted(result.keys())])
            
    def __neg__(self):
        return Polynomial([-self._terms[i] for i in sorted(self._terms.keys())])
        
    def __sub__(self, other):
        if type(other) != Polynomial:
            other = Polynomial([other])
        return self + (-other)
        
    def __mul__(self, other):
        result = {}
        if type(other) != Polynomial:
            other = Polynomial([other])
        for arg1 in sorted(self._terms.keys()):
            for arg2 in sorted(other._terms.keys()):
                if arg1 + arg2 not in result:
                    result[arg1 + arg2] = 0
                result[arg1 + arg2] += self._terms[arg1] * other._terms[arg2]
        return Polynomial([result[i] if i in result else 0 for i in range(max(result.keys()) + 1)])
    
    def __pow__(self, other):
        result = 1
        for i in range(other):
            result = self * result
        return result
    
    def degree(self):
        return max(self._terms.keys())
        
    def find_roots(self):
        pass
        
    def derive(self):
        result = self._terms.copy()
        for var in sorted(result.keys()):
            if var == 0:
                continue
            result[var-1] = var * result[var]
        result.pop(max(result.keys()))
        return Polynomial([result[i] for i in sorted(result.keys())])
    
    def integrate(self, cons = 0):
        result = self._terms.copy()
        for var in sorted(result.keys())[::-1]:
            result[var + 1] = result[var]/(var + 1)
        result[0] = cons
        return Polynomial([result[i] for i in sorted(result.keys())])
    
    def evaluate(self, num):
        result = 0
        for i in self._terms:
            result += self._terms[i] * num ** i
        return result
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    