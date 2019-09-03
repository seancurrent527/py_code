'''
tictactoe.py
'''

import sys
import math
import random

class Tree:
    def __init__(self, val):
        self._val = val
        self._children = []
        self._winval = is_winner(self._val)
        
    def __str__(self):
        return str(self._val) + ' : ' + str(self._winval)
        
    def __repr__(self):
        return str(self)
        
    def add_child(self, node):
        self._children.append(node)
    
    def descend(self, child):
        for grid in self._children:    
            if grid._val == child:
                return grid
    
    def __getitem__(self, n):
        return self._children[n]
    
    def best_path(self, level=10, drop=1, CONSTANT=10):
        if level == CONSTANT and self._children:
            
            for i in range(len(self._children)):
                if is_winner(self._children[i]._val) == -1:
                    return i
        
            return min([(self._children[i].best_path(level - drop, drop),i) for i in range(len(self._children))])[1]
        if not self._children:
            return level * self._winval
        var = [self._children[i].best_path(level - drop, drop) for i in range(len(self._children))]
        if level % 2 == 0:
            return min(var)# * var.count(min(var))
        else: 
            return max(var)# * var.count(max(var))
       
def is_winner(vec):
    for x in (1,-1):
        for i in range(3):
            if sum(vec[3*i:3*i+3]) == 3*x or sum(vec[i::3]) == 3*x:
                return x
        if vec[0]==vec[4]==vec[8]==x or vec[2]==vec[4]==vec[6]==x:
            return x
    return 0
    
def initialize_AI(root, play_first = False):
    x = -1 if play_first else 1
    for i in range(9):
        curr = root._val.copy()
        if curr[i] == 0:
            curr[i] = x
            root.add_child(Tree(curr))
    for tr in [g for g in root._children if is_winner(g._val) == 0]:
        initialize_AI(tr, not play_first)

def player_input(board):
    spot = input('Where would you like to play: (row,column) ')
    if spot == 'Terminate AI protocol tic-tac-toe':
        print('Error: AI Beaten -- Player wins!')
        sys.exit(1)
    spot = [int(x) - 1 for x in spot.split(',')]
    spot = spot[0] * 3 + spot[1]
    if board[spot] != 0:
        print('You cannot play there.')
        player_input(board)
    else:
        board[spot] = 1
    
def print_board(board, key):
    result = '\n'
    for i in range(3):
        curr = board[i*3:i*3+3]
        curr = [key[0] if x == 1 else x for x in curr]
        curr = [key[1] if x == -1 else x for x in curr]
        curr = [' ' if x == 0 else x for x in curr]
        result += '|'.join(curr) + '\n'
        if i != 2: result += '-+-+-' + '\n'
    print(result)
    
    
#===============================================================================
def main():

    sys.setrecursionlimit(1500)
    
    board = [0 for i in range(9)]
    choice = input('Play as X or O? (x|o) ').lower()
    if choice == 'x':
        KEY = ('X', 'O')
    else:
        KEY = ('O', 'X')
    
    comp = Tree(board)
    
    PLAY_FIRST = random.choice([True, False])
    
    initialize_AI(comp, PLAY_FIRST)
    
    if PLAY_FIRST:
        print('The computer will play first.')
        board = comp._children[comp.best_path()]._val
        comp = comp.descend(board)
        print_board(board, KEY)
    else:
        print('The player will play first.')
        print_board(board, KEY)
        
    while not is_winner(board):
    
        player_input(board)
        comp = comp.descend(board)
        print_board(board, KEY)
        if is_winner(board) == 0  and 0 not in board:
            print('Tie Game!!!')
            return
        if not is_winner(board):
            print('Computer\'s turn:')
            board = comp._children[comp.best_path()]._val
            comp = comp.descend(board)
            print_board(board, KEY)
        if is_winner(board) == 0  and 0 not in board:
            print('Tie Game!!!')
            return
            
    WINNER = 'Computer' if is_winner(board) == -1 else 'PLAYER'
    
    print('The', WINNER, 'won!!!')
    
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    