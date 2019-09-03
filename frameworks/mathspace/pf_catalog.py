'''
probability.py
'''

import math

factorial = lambda n: 1 if n <= 1 else n * factorial(n - 1)

choose = lambda n, k: factorial(n)/(factorial(k) * factorial(n - k))

#DISCRETE

def bernoulli(k, p):
    if k == 1:
        return p
    if k == 0:
        return 1-p
    else:
        return 0
   
def binomial(k, p, n):
    return choose(n, k) * p ** k * (1 - p) ** (n - k)
    
def poisson(k, l):
    return math.e ** (-l) * l ** k / factorial(k)
    
def geometric(k, p):
    return p * (1 - p) ** (k - 1)
    
def negative_binomial(k, p, n):
    assert k >= n, "k must be in the set {n, n + 1, n + 2,...}"
    return choose(k - 1, n - 1) * p ** n * (1 - p) ** (k - n)
    
#CONTINUOUS    
    
    
    
#====================================================================================
def main():

    '''
    p_dict = {-4 : 0.1, -1 : 0.05, 0 : 0.35, 2 : 0.3, 4 : 0.15, 5 : 0.1, 6 : 0.05}
    pmf = mass_function(p_dict)
    print(probability(pmf, min = 1))
    print(probability(pmf, min = -100, condition = lambda x: x % 2 == 1))
    print(conditional_probability(pmf, min = -100, condition = lambda x: x >= 3, given = lambda x: x > 0))
    print(expected_value(pmf, min = -100))
    '''
    
    '''
    pmf = mass_function(binomial, 0.5, 3)
    print(expected_value(pmf, max = 3))
    print(variance(pmf, max = 3))
    print(expected_value(pmf, operator = lambda x: x**2, max = 3))
    print(variance(pmf, operator = lambda x: x**2, max = 3))
    '''
    
    '''
    pmf = mass_function(poisson, 2)
    print(probability(pmf, condition = lambda x: x >= 1 and x <= 3))
    print(probability(pmf, min = 3))
    print(probability(pmf, condition = lambda x: x >= 3))
    print(probability(pmf, condition = lambda x: x % 2 == 0))
    '''
    
    
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    