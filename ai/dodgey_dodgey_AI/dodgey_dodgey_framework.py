'''
Framework for dodgey_dodgey.
'''

import random, numpy as np, time

class Arrow:
    def __init__(self, field_size):
        self.field = field_size
        inner = [i+1 for i in range(self.field)]
        form = {(0,1): (random.choice(inner), 0, np.array([1,0,0,0,0])),
                (0,-1): (random.choice(inner), self.field + 1, np.array([0,1,0,0,0])),
                (1,0): (0, random.choice(inner), np.array([0,0,1,0,0])),
                (-1,0): (self.field + 1, random.choice(inner), np.array([0,0,0,1,0]))}
        temp = random.choice(list(form.keys()))
        self.dir = temp
        self.x, self.y, self.vector = form[self.dir]
        self.id = self.vector.argmax()
        self._x = None
        self._y = None

    def __str__(self):
        return 'v^><'[self.id]

    def __eq__(self, other):
        return self.dir == other.dir and self.x == other.x and self.y == other.y

    def move(self, grid):
        self._x, self._y = self.x, self.y
        self.x += self.dir[0]
        self.y += self.dir[1]
        grid[self.y, self.x] += self.vector
        grid[self._y, self._x] -= self.vector

    def undo(self, grid):
        self._x, self._y = self.x, self.y
        self.x -= self.dir[0]
        self.y -= self.dir[1]
        grid[self.y, self.x] += self.vector
        grid[self._y, self._x] -= self.vector

    def in_field(self):
        return min(self.x, self.y) >= 0 and max(self.x, self.y) <= self.field + 1

class Player:
    def __init__(self, field_size):
        self.field = field_size
        self.x = self.y = field_size // 2 + 1
        self.move_dict = {'w': (0,-1), 'a': (-1,0), 's': (0,1), 'd': (1,0)}
        self.vector = np.array([0,0,0,0,1])

    def __str__(self):
        return 'P'

    def move(self, grid, char):
        self._x, self._y = self.x, self.y
        self.x += self.move_dict[char][0]
        self.y += self.move_dict[char][1]
        grid[self.y, self.x] += self.vector
        grid[self._y, self._x] -= self.vector

    def undo(self, grid, char = None):
        if char:
            opposite = {'w':'s', 'a':'d', 'd':'a', 's':'w'}
            self.move(grid, opposite[char])
        else:
            grid[self.y, self.x] -= self.vector
            self.x, self.y = self._x, self._y
            grid[self.y, self.x] += self.vector

    def in_field(self):
        return min(self.x, self.y) >= 1 and max(self.x, self.y) <= self.field

class GameGrid:
    def __init__(self, field_size):
        self.field_size = field_size
        self.player = Player(field_size)
        self.obstacles = []
        self.grid = np.zeros((self.field_size + 2, self.field_size + 2, 5))
        self.grid[self.player.y, self.player.x, 4] = 1
        self.turn = 0
        self.past_moves = []

    def __str__(self):
        def print_char(x):
            if (x == np.array([0,0,0,0,1])).all():
                return 'P'
            if sum(x) == 0:
                return ' '
            if x[-1] == 1 and sum(x) >= 2:
                return 'O'
            if sum(x) >= 2:
                return 'X'
            else:
                return 'v^><'[x.argmax()]
        retval = 'Turn: ' + str(self.turn) + '\n'
        retval += ' '.join([print_char(x) for x in self.grid[0]]) +  '\n'
        for i in range(1, self.field_size + 1):
            retval += ' ' + '-'.join('+' * (self.field_size + 1)) + ' \n' 
            retval += '|'.join([print_char(x) for x in self.grid[i]]) + '\n'
        retval += ' ' + '-'.join('+' * (self.field_size + 1)) + ' \n' 
        retval += ' '.join([print_char(x) for x in self.grid[self.field_size + 1]])
        return retval

    def cont(self):
        return (self.grid[self.player.y, self.player.x] == np.array([0,0,0,0,1])).all()

    def __copy__(self):
        pass

    def move(self, char):
        opposite = {'w':'s', 'a':'d', 'd':'a', 's':'w'}
        self.turn += 1
        self.player.move(self.grid, char)
        if not self.player.in_field():
            self.player.move(self.grid, opposite[char])
            self.turn -= 1
            return False
        self.past_moves.append(char)
        for i in range(len(self.obstacles)):
            obs = self.obstacles[i]
            if obs is not None:
                try:
                    obs.move(self.grid)
                except IndexError:
                    self.grid[obs._y, obs._x] -= obs.vector
                    self.obstacles[i] = None
        return True

    #DOES NOT WORK
    def undo(self):
        self.turn -= 1
        self.player.undo(self.grid, self.past_moves.pop())
        for obs in self.obstacles:
            if obs is not None:
                obs.undo(self.grid)
    

    def add_obstacles(self):
        for i in range(self.turn//20 + 1):
            obs = Arrow(self.field_size)
            if not self.obstacles or obs != self.obstacles[-1]:
                self.grid[obs.y, obs.x] += obs.vector
                self.obstacles.append(obs)

def play_game(board, computer = None, printing = True, sleep = 0):
    penalty = 0
    limit = 5
    while board.cont():
        printing and print(board)
        sleep and time.sleep(sleep)
        choice = input().lower() if computer is None else computer(board)
        if choice == 'undo':
            board.undo()
            penalty += 5
        if not choice or choice[0] not in 'wasd' or not board.move(choice[0]):
            printing and print('That is not a valid move.')
            penalty += 0
            limit -= 1
            if limit == 0:
                return board.turn - 5*penalty
            continue
        board.add_obstacles()
        limit = 5
    printing and print(board)
    return board.turn - penalty

#=========================================================================
def main():
    printing = True
    grid = GameGrid(7) #int(input('Size: ')))
    score = play_game(grid, printing = printing)
    printing and print('---', 'Your score is:', score, '---')


if __name__ == '__main__':
    main()