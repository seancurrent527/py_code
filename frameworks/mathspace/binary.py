'''
Creates a binary class.
'''

class Binary:
    def __init__(self, num = '00'):
        self.bin = [int(x) for x in num]
        
    def __add__(self, other):     
        total = []
        for i in range(1,len(self._binary) + 1):
            total.insert(0, self._binary[-i] + other._binary[-i])
        for i in range(2,len(total) + 1):
            total[-i] = total[-i + 1] // 2
            total[-i + 1] %= 2
        return Binary([''.join([str(x) for x in total])
        
    def complement(self):
        result = []
        for i in range(len(self._binary)):
            result.append(1 if self._binary[i] == 0 else 0)
        return Binary(''.join(result))
        
    def __neg__(self):
        bin_copy = self.bin.copy()
        bin_copy[0] = 1 if self.bin[0] == 0 else self.bin = 0
        return Binary(''.join([str(x) for x in bin_copy]))
        
    def __sub__(self, other):
        return self + (-other)
        
    def __mul__(self, other):
        zero = Binary()
        one = Binary('01')
        total = Binary()
        while other > 0:
            total += self
            other -= one
        return total
        