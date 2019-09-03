'''
MATHSPACE
'''

import inspect
import math
import random

class Fraction:
    def __init__(self, num = 1, den = 1):
        assert den != 0, "ERROR: Denominator cannot be zero"
        self._nu = num
        self._de = den
        self.simplify()
       
    def __str__(self):
        return '(' + str(self._nu) + '/' + str(self._de) if self._de != 1 else str(self._nu) + ')'
        
    def __repr__(self):
        return str(self)
        
    def rationalize(self):
        while self._nu % 1 and self._de % 1:
            self._nu *= 10
            self._de *= 10
        self._nu = int(self._nu)
        self._de = int(self._de)
        
    def decimal(self):
        return self._nu / self._de
        
    def reduce(self):
        for i in range(1, self._nu + 1):
            if self._nu % i == 0 and self._de % i == 0:
                self._nu //= i
                self._de //= i
            if self._nu == 1 or self._de == 1:
                return

    def simplify(self):
        self.rationalize()
        self.reduce()
        
    def __int__(self):
        return int(self.decimal())
        
    def __float__(self):
        return self.decimal()
        
    def __abs__(self):
        return Fraction(abs(self._nu), abs(self._de))
        
    def __mul__(self, other):
        if type(other) == Fraction:
            return Fraction(self._nu * other._nu, self._de * other._de)
        if type(other) in (int, float):
            return Fraction(self._nu * other, self._de) if self._de != 1 else self._nu * other
        if type(other) == Complex:
            return Complex(self * other._re, self * other._im)
        else: return other * self
        
    def __rmul__(self, other):
        return self * other
        
    def __add__(self, other):
        if type(other) == Fraction:
            retval = Fraction(self._nu * other._de + other._nu * self._de, self._de * other._de)
        else:
            retval = Fraction(self._nu + other * self._de, self._de)
        retval.simplify()
        return retval
    
    def __radd__(self, other):
        if type(other) == Fraction:
            retval = Fraction(self._nu * other._de + other._nu * self._de, self._de * other._de)
        else:
            retval = Fraction(self._nu + other * self._de, self._de)
        retval.simplify()
        return retval
    
    def __sub__(self, other):
        return self + (-other)
    
    def __invert__(self):
        return Fraction(self._de, self._nu)
    
    def __pow__(self, n):
        return Fraction(self._nu ** n, self._de ** n)
    
    def __truediv__(self, other):
        if type(other) == Fraction:
            return self * ~other
        else:
            return Fraction(self._nu, self._de * other)
            
    def __rtruediv__(self, other):
        return other * ~self 
            
    def __neg__(self):
        return Fraction(-self._nu, self._de)
    
    
#===============================================================================

class Complex:
    def __init__(self, real=0, imag=0):
        if type(real) == Complex:
            self._re = real._re
            self._im = real._im
        else:
            self._re = real
            self._im = imag
        
    def __str__(self):
        real, imag = self._re, self._im
        if int(real) == real: real = int(real)
        if int(imag) == imag: imag = int(imag)
        if self._im == 0:
            return '(' +  str(real) + ')'
        elif self._re == 0:
            return '(' + str(imag) + 'i' + ')'
        return '(' + str(real) + ' + ' + str(imag) + 'i' + ')'
        
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
        return round(Complex(self._re / abs(self) ** 2, -self._im / abs(self) ** 2), 6)
        
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
        
    def magnitude(self):
        return math.sqrt(self._re ** 2 + self._im **2)
    
    def angle(self):
        return math.atan(self._im/self._re)
    
    def get_real(self):
        return self._re
        
    def get_imag(self):
        return self._im
        
    def __round__(self, n):
        return Complex(round(self._re, n), round(self._im, n))
        
def sqrt(num):
    if type(num) == Fraction:
        return Fraction(sqrt(num._nu), sqrt(num._de))
    return math.sqrt(num) if num >= 0 else Complex(0, math.sqrt(-num))
    
    
#==============================================================================    

#========================================================================================

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
    
    def __abs__(self):
        return sqrt(sum(x**2 for x in self._vec))
    
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
    
    
#==============================================================================


class Matrix:

    ROUND_VAL = 3

    def __init__(self, lol = [[]]):
        if True not in [type(x) == list for x in lol]:
            self._grid = [[Complex(lol[i][j]) for i in range(len(lol))] for j in range(len(lol[0]))]        
        else:
            self._grid = [[Complex(n) for n in row] for row in lol] 
        self._rdim = len(self._grid)
        self._cdim = len(self._grid[0])

    def __len__(self):
        return self._rdim
        
    def __str__(self):
        result = ''
        for l in self._grid:
            result += '[ '
            num_list = []
            for num in l:
                num_list.append(str(round(num, Matrix.ROUND_VAL)).center(max([len(str(round(n, Matrix.ROUND_VAL))) for n in self._list()]) + 2))
            result += ' '.join(num_list) + ' ]\n'
        return result
        
    def __repr__(self):
        #result = 'Matrix(' + str(self._grid) + ')'
        result = str(self)
        return result
        
    def _list(self):
        result = []
        for i in range(len(self)):
            result += self[i]
        return result

    def __hash__(self):
        return hash(str(list(self)))
    
    def __add__(self, other):
        assert self._cdim == other._cdim and self._rdim == other._rdim, 'ERROR: Matrix dimensions must match.'
        result = [[self._grid[j][i] + other._grid[j][i] for i in range(self._cdim)] for j in range(self._rdim)]
        return Matrix(result)

    def new_scale(self, n):
        result = [[self._grid[j][i] * n for i in range(self._cdim)] for j in range(self._rdim)]
        return Matrix(result)
        
    def scale(self, n):
        self._grid = [[self._grid[j][i] * n for i in range(self._cdim)] for j in range(self._rdim)]
    
    def __mul__(self, other):
        if type(other) != Matrix:
            if type(other) == Vector:
                return Vector([self.row(i) * other for i in range(self._cdim)])
            else:
                result = [[self[i][j] * other for j in range(self._cdim)] for i in range(self._rdim)]
        else:
            assert self._cdim == other._rdim, 'ERROR: Matrix dimensions must match.'
            result = [[self.row(i) * other.col(j) for j in range(other._cdim)] for i in range(self._rdim)]
        return Matrix(result)    
    
    def __rmul__(self, other):
        return self * other
    
    def __truediv__(self, other):
        return self * (1/other)
    
    def __neg__(self):
        return self.new_scale(-1)
        
    def __sub__(self, other):
        return self + (-other)
        
    def __eq__(self, other):
        return str(self) == str(other)
        
    def __getitem__(self, n):
        return self._grid[n]
        
    def row(self, i):
        return Vector(self._grid[i])
        
    def col(self, i):
        return Vector([row[i] for row in self._grid])
        
    def transpose(self):
        return Matrix([self.row(i) for i in range(len(self._grid))])
        
    def conjugate(self):
        grid = [[num.conjugate() for num in row] for row in self._grid]
        return Matrix(grid)
    
    def adjoint(self):
        return self.conjugate().transpose()
        
    def is_identity(self):
        return self == Matrix.identity(self._rdim)
        
    def is_orthogonal(self):
        return (self.transpose()*self).is_identity()
    
    def is_symmetric(self):
        return self == self.transpose()
        
    def is_hermitian(self):
        return self == self.adjoint()
        
    def is_unitary(self):
        return (self.adjoint()*self).is_identity()
        
    def is_normal(self):    
        return self*self.adjoint() == self.adjoint()*self
        
    def is_square(self):
        return self._rdim == self._cdim
        
    def permute(self, r1, r2):
        self[r1], self[r2] = self[r2], self[r1]
   
#fix zeroes as pivots
   
    def ref(self): #fix permutations with zero rows and missing pivots!
        retval = []
        for i in range(len(self)):
            result = self.row(i)
            for j in range(len(retval)):
                ro = retval[j]
                if ro[j] == 0:
                    continue
                result = result - (result[j]/ro[j]) * ro
            if i < len(result) and result[i] != 0:
                retval.append(result/result[i])
            else:
                retval.append(result)
        return Matrix([list(v) for v in retval])
        
    def rref(self): #still not perfect, only works when rows < cols
        retval = []
        echelon = self.ref()
        dim = min(echelon._rdim, echelon._cdim)
        for i in range(len(echelon) - 1, -1, -1):
            result = echelon.row(i)
            for j in range(len(retval)):            
                ro = retval[j]
                if ro[dim - 1 - j] == 0:
                    continue  
                result = result - (result[dim-1-j]/ro[dim-1-j]) * ro    
            retval.append(result)
        return Matrix([list(v) for v in retval[::-1]])
        
    def augment(self, other):
        if type(other) == Vector:
            return Matrix([self.col(i) for i in range(self._cdim)] + [other])
        return Matrix([self.col(i) for i in range(self._cdim)] + [other.col(i) for i in range(other._cdim)])
        
    def deaugment(self, colnum):
        assert type(colnum) == int, "colnum must be an integer."
        return Matrix([r[:colnum] for r in self]), Matrix([r[colnum:] for r in self]) 
    
    def inverse(self):
        assert self.is_square()
        aug = self.augment(Matrix.identity(len(self)))
        return aug.rref().deaugment(len(self))[1]
    
    @classmethod
    def zeroes(cls, n):
        return cls([[0 for i in range(n)] for j in range(n)])
        
    @classmethod
    def identity(cls, n):
        retval = [[0 for i in range(n)] for j in range(n)]
        for i in range(n):
            retval[i][i] = 1
        return cls(retval)
        
    @classmethod
    def rand(cls, n, min = 0, max = 0, field = 'real'):
        if not max: max = 100 if field == 'real' else 10
        if field.lower() in ('r', 'real'):
            return cls([[random.randrange(min, max) for i in range(n)] for j in range(n)])
        if field.lower() in ('c', 'complex', 'i', 'imaginary'):
            return cls([[Complex(random.randrange(min, max), random.randrange(min, max)) \
                for i in range(n)] for j in range(n)])
        
    @classmethod
    def set_ROUND_VAL(cls, n):
        ROUND_VAL = n
    
# add diagonalization
# add eigenstuff
# add null and range
        
        
#==============================================================================        
        
#CONSTANTS
i = Complex(0,1)        
M = Matrix

a = Fraction(1,2)
b = Fraction(1,4)
c = Fraction(1,3)
d = Fraction(2,3)
e = Fraction(3,2)
    
#==============================================================================    
    
I = Matrix([[1,0,0],[0,1,0],[0,0,1]])
A = Matrix([[1,2,0],[0,1,0],[0,0,1]])
B = Matrix([[3,0,0],[1/2,2,0],[1,0,1]])
C = Matrix([[Complex(1,1), Complex(0,1), 0],[0,1,0],[Complex(0,-1),0,1]])
V = Vector([1,1,2])















    
    
    
    