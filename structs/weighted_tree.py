import numpy as np
import sys

class WeightedNode:
    def __init__(self, datum):
        self.datum = datum
        self.left = None
        self.right = None
        self.lweight = 0
        self.rweight = 0

    def add_left(self, datum):
        self.left = WeightedNode(datum)
        self.lweight += 1

    def add_right(self, datum):
        self.right = WeightedNode(datum)
        self.rweight += 1

    def add(self, datum, descending = False):
        comp = lambda x, y: x < y if not descending else lambda x, y: x > y
        if comp(self.datum, datum):
            if self.right is None:
                self.add_right(datum)
            else:
                self.right.add(datum, descending=descending)
                self.rweight += 1
        else:
            if self.left is None:
                self.add_left(datum)
            else:
                self.left.add(datum, descending=descending)
                self.lweight += 1

    def fill_array(self, arr):
        fulcrum = self.lweight
        arr[fulcrum] = self.datum
        if self.left:
            assert self.lweight > 0
            self.left.fill_array(arr[:fulcrum])
        if self.right:
            assert self.rweight > 0
            self.right.fill_array(arr[fulcrum + 1:])
        

class WeightedTree:
    def __init__(self, datum = None):
        self.root = None
        self.weight = 0
        if datum:
            self.root = WeightedNode(datum)
            self.weight += 1
        
    def add(self, datum, descending = False):
        if self.root is None:
            self.root = WeightedNode(datum)
            self.weight += 1
        else:
            self.root.add(datum, descending=descending)
            self.weight += 1

    def to_array(self):
        arr = np.empty(self.weight, dtype=object)
        if self.root is None:
            return arr
        self.root.fill_array(arr)
        return arr

def main():
    sys.setrecursionlimit(1000)
    test_array = np.random.randint(1, 20, size = 10000)
    weighted_tree = WeightedTree()
    print(test_array)
    [weighted_tree.add(dat) for dat in test_array]
    print(weighted_tree.to_array())
    print(np.sort(test_array))

if __name__ == '__main__':
    main()