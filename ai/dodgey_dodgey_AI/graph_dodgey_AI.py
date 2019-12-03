'''
tictactoe.py
'''

import sys
import math
import random
import copy
import dodgey_dodgey_framework as ddf

class Tree:
    def __init__(self, val, move = None):
        self._val = val
        self._move = move
        self._children = []
        
    def __str__(self):
        return str(self._move) + ' : ' + str(self._val)
        
    def __repr__(self):
        return str(self)
        
    def add_child(self, node):
        self._children.append(node)
    
    def __getitem__(self, n):
        return self._children[n]
    
    def still_alive(self):
        return self._val.cont()

    def best_path(self, depth = 5, return_move = True):
        if depth == 0 and self.still_alive():
            return 1
        elif not self.still_alive():
            return 0
        moves = 'wasd'
        for i in range(4):
            curr = copy.deepcopy(self._val)
            add = curr.move(moves[i])
            if add:
                self.add_child(Tree(curr, moves[i]))
        if not return_move:
            return 1 / (3 ** depth) + sum([child.best_path(depth - 1, return_move = False) for child in self._children])
        elif return_move:
            return max([(child.best_path(depth - 1, return_move = False), child._move) for child in self._children])[1]
    
#===============================================================================
def main():

    sys.setrecursionlimit(1500)
    
    grid = ddf.GameGrid(7)
    score = 0
    while grid.cont():
        root = Tree(grid, 'root')
        best_move = root.best_path(depth = 5)
        grid.move(best_move)
        score += 1
        grid.add_obstacles()
        print(best_move)
        print(grid)
    print('---', 'Your score is:', score, '---')

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    