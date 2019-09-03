'''
Implementaion for probability classes
'''

'''
probability.py
'''

import math, matplotlib.pyplot as plt, pf_catalog, numpy as np

factorial = lambda n: 1 if n <= 1 else n * factorial(n - 1)

choose = lambda n, k: factorial(n)/(factorial(k) * factorial(n - k))

discrete = lambda a, b: range(math.floor(a), math.ceil(b))

def SimpsonsRule(func, xmin, xmax, bins):
    dx = (xmax - xmin)/bins
    partition = [xmin + i * dx for i in range(1, bins)]
    summation = func(xmin) + func(xmax)
    four = True
    for value in partition:
        factor = 2 + 2 * four; four = not four
        summation += factor * func(value)
    return dx/3 * summation

class MassFunction:
    def __init__(self, func, args = [], domain = range(0, 1000)):
        if type(func) == dict:
            self.pmf = lambda x: func[x] if x in func else 0
        else:
            self.pmf = lambda x: func(x, *args)
        self.domain = domain
        self._ev = self.expected_value()
        self._var = self.variance()
        self._std = self.std_deviation()
        
    def probability(self, *vals, condition = lambda x: True):
        return sum(self.pmf(v) for v in (vals if vals else self.domain) if condition(v))
    
    def conditional_probability(self, *vals, condition = lambda x: True, given = lambda x: True):
        intersection = sum(self.pmf(v) for v in (vals if vals else self.domain) if condition(v) and given(v))
        conditional = self.probability(*(vals if vals else self.domain), condition = given)
        return intersection / conditional
        
    def expected_value(self, *vals, operator = lambda x: x, condition = lambda x: True):
        return sum(self.pmf(v) * operator(v) for v in (vals if vals else self.domain) if condition(v))
        
    def variance(self, *vals, operator = lambda x: x, condition = lambda x: True):
        return self.expected_value(*(vals if vals else self.domain), operator = lambda x: operator(x) ** 2, condition = condition) - \
            self.expected_value(*(vals if vals else self.domain), operator = operator, condition = condition) ** 2
            
    def std_deviation(self, *vals, operator = lambda x: x, condition = lambda x: True):
        return self.variance(*(vals if vals else self.domain), operator = operator, condition = condition) ** 0.5
 
    def view(self, minval = None, maxval = None):
        if minval is None:
            minval = max(0, self._ev - 3 * self._std)
        if maxval is None:
            maxval = self._ev + 3 * self._std
        probs = [self.probability(val) if val in self.domain else 0 for val in discrete(minval, maxval)]
        plt.bar(discrete(minval, maxval), probs)
        plt.show()
 
class DensityFunction:
    def __init__(self, func, args = [], xmin = -100, xmax = 100):
        self.pdf = lambda x: func(x, *args)
        self.xmin = xmin
        self.xmax = xmax
        self._ev = self.expected_value()
        self._var = self.variance()
        self._std = self.std_deviation()
        
    def probability(self, xmin = None, xmax = None, bins = 30):
        if xmin is None: xmin = self.xmin
        if xmax is None: xmax = self.xmax
        return SimpsonsRule(self.pdf, xmin, xmax, bins)
    
    def expected_value(self, operator = lambda x: x, bins = 30):
        func = lambda x: operator(x) * self.pdf(x)
        return SimpsonsRule(func, self.xmin, self.xmax, bins)
        
    def variance(self, operator = lambda x: x, bins = 30):
        return self.expected_value(lambda x: operator(x) ** 2, bins = bins) - self.expected_value(operator, bins = bins) ** 2 
            
    def std_deviation(self, operator = lambda x: x, bins = 30):
        return self.variance(operator, bins = bins) ** 0.5
 
    def view(self, minval = None, maxval = None, detail = 100):
        if minval is None:
            minval = self._ev - 3 * self._std
        if maxval is None:
            maxval = self._ev + 3 * self._std
        step = (maxval - minval)/100
        indep = np.arange(minval, maxval, step)
        plt.plot(indep, self.pdf(indep))
        plt.show()
 
 
#====================================================================================
 
def main():
    
    '''
    p_dict = {-4 : 0.1, -1 : 0.05, 0 : 0.35, 2 : 0.3, 4 : 0.15, 5 : 0.1, 6 : 0.05}
    pmf = MassFunction(p_dict, domain = range(-4, 7))
    print(pmf.probability(condition = lambda x: x > 0))
    print(pmf.probability(condition = lambda x: x % 2 == 1))
    print(pmf.conditional_probability(condition = lambda x: x >= 3, given = lambda x: x > 0))
    print(pmf.expected_value())
    
    from pmf_catalog import binomial
    from pmf_catalog import poisson
    
    pmf = MassFunction(binomial, 0.5, 3, domain = range(0, 4))
    print(pmf.expected_value())
    print(pmf.variance())
    print(pmf.expected_value(operator = lambda x: x**2))
    print(pmf.variance(operator = lambda x: x**2))
    
    pmf = MassFunction(poisson, 2, domain = range(0, 100))
    print(pmf.probability(condition = lambda x: x >= 1 and x <= 3))
    print(pmf.probability(condition = lambda x: x >= 3))
    print(pmf.probability(condition = lambda x: x >= 3))
    print(pmf.probability(condition = lambda x: x % 2 == 0))
    '''
    
    
if __name__ == '__main__':
    main()   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
