'''
Matrix class setup.
'''

from vectors import *
from complex import *

class Matrix:
    def __init__(self, lol = [[]]):
        if True not in [type(x) == list for x in lol]:
            self._grid = [[Complex(lol[i][j]) for i in range(len(lol))] for j in range(len(lol[0]))]        
        else:
            self._grid = [[Complex(lol[j][i]) for i in range(len(lol))] for j in range(len(lol[0]))]
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
                num_list.append(str(num).center(max([len(str(n)) for n in self._list()]) + 2))
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
        return self._grid == other._grid
        
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
        identity = True
        for i in range(self._rdim):
            for j in range(self._cdim):
                if i != j and self[i][j] != 0:
                    identity = False
                if i == j and self[i][j] != 1:
                    identity = False
        return identity
        
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
        
    def permute(self, r1, r2):
        self._grid[r1], self._grid[r2] = self._grid[r2], self._grid[r1]
    
    def ref(self):
        retval = []
        for i in range(len(self)):
            result = self.row(i)
            for j in range(i):
                ro = retval[j]
                if ro[j] == 0:
                    continue
                result = result - (result[j]/ro[j]) * ro
            if result[i] != 0:
                retval.append(result/result[i])
            else:
                retval.append(result)
        return Matrix([list(v) for v in retval])
    
    def rref(self):
        retval = []
        echelon = self.ref()
        for i in range(len(echelon) - 1, -1, -1):
            result = echelon.row(i)
            for j in range(len(retval)):
                ro = retval[j]
                if ro[len(ro) - 1 - j] == 0:
                    continue
                result = result - (result[len(ro)-1-j]/ro[len(ro)-1-j]) * ro    
            retval.append(result)
        return Matrix([list(v) for v in retval[::-1]])

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
    
    
    

















