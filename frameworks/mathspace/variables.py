'''
Test implementation for variables in mathspace.
'''

class Variable:
    def __init__(self, name):
        self.name = name
        self.function_stack = []
        self._var = self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Variable(' + self.name + ')'

    def add_function(self, function, *args):
        self.function_stack.append(lambda x: function(x, *args))

    def evaluate(self, val):
        num = val
        for func in self.function_stack:
            num = func(num)
        if type(num) == Variable and num._var == self._var:
            return num.evaluate(val)
        return num

    def __add__(self, other):
        result = Variable('(' + self.name + ' + ' + str(other) + ')')
        result.function_stack = self.function_stack.copy()
        result._var = self._var
        result.add_function(lambda x, a: x + a, other)
        return result

    def __sub__(self, other):
        result = Variable('(' + self.name + ' - ' + str(other) + ')')
        result.function_stack = self.function_stack.copy()
        result._var = self._var
        result.add_function(lambda x, a: x - a, other)
        return result

    def __mul__(self, other):
        result = Variable('(' + self.name + ' * ' + str(other) + ')')
        result.function_stack = self.function_stack.copy()
        result._var = self._var
        result.add_function(lambda x, a: x * a, other)
        return result

    def __abs__(self):
        result = Variable('abs(' + self.name + ')')
        result.function_stack = self.function_stack.copy()
        result._var = self._var
        result.add_function(lambda x: abs(x))
        return result

    def __pow__(self, other):
        result = Variable('(' + self.name + ' ** ' + str(other) + ')')
        result.function_stack = self.function_stack.copy()
        result._var = self._var
        result.add_function(lambda x, a: x ** a, other)
        return result

    def __truediv__(self, other):
        result = Variable('(' + self.name + ' / ' + str(other) + ')')
        result.function_stack = self.function_stack.copy()
        result._var = self._var
        result.add_function(lambda x, a: x / a, other)
        return result

    def __neg__(self):
        result = Variable('(-' + self.name + ')')
        result.function_stack = self.function_stack.copy()
        result._var = self._var
        result.add_function(lambda x : -x)
        return result

    def __radd__(self, other):
        result = Variable('(' + str(other) + ' + ' + self.name + ')')
        result.function_stack = self.function_stack.copy()
        result._var = self._var
        result.add_function(lambda x, a: a + x, other)
        return result

    def __rmul__(self, other):
        result = Variable('(' + str(other) + ' * ' + self.name + ')')
        result.function_stack = self.function_stack.copy()
        result._var = self._var
        result.add_function(lambda x, a: a * x, other)
        return result

    def __rsub__(self, other):
        result = Variable('(' + str(other) + ' - ' + self.name + ')')
        result.function_stack = self.function_stack.copy()
        result._var = self._var
        result.add_function(lambda x, a: a - x, other)
        return result

    def __rtruediv__(self, other):
        result = Variable('(' + str(other) + ' / ' + self.name + ')')
        result.function_stack = self.function_stack.copy()
        result._var = self._var
        result.add_function(lambda x, a: a / x, other)
        return result

    def __invert__(self):
        return 1 / self

    def __getitem__(self, n):
        return self.evaluate(n)
















