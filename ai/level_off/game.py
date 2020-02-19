import objects
from utils import Actions, Levels
import numpy as np

class GameState:
    def __init__(self, format_string):
        self.blocks = []
        self.holes = []
        self.walls = []
        grid = format_string.split('\n')
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                self.filterValue(grid[r][c], (r, c))
        self.size = (r, c)
        self.grid = np.full(self.size, None, dtype=object)
        self.grid[self.getPlayerPosition()] = self.player

    def __str__(self):
        string_list = []
        for row in self.grid:
            string_list.append([])
            for item in row:
                if type(item) is objects.Wall:
                    string_list[-1].append('#')
                elif item is None:
                    string_list[-1].append(' ')
                elif type(item) is objects.Player:
                    string_list[-1].append('P')
                else:
                    string_list[-1].append(Levels.symbols[item.size])
        return '\n'.join([''.join(ls) for ls in string_list])

    def getWalls(self):
        return self.walls

    def getBlocks(self):
        return self.blocks

    def getHoles(self):
        return self.holes

    def getPlayer(self):
        return self.player

    def getPlayerPosition(self):
        return self.player.position

    def getSize(self):
        return self.size

    def getGrid(self):
        return self.grid

    def move(self, direction):
        vector = Actions.ACTIONS[direction]
        self.movePlayer(vector)

    def movePlayer(self, vector):
        origin = self.player.position
        position = self.player.move(vector)
        if self.grid[position] is not None:
            self.moveBlock(self.grid[position], vector)
        self.grid[position] = self.player
        self.grid[origin] = None

    def moveBlock(self, block, vector):
        origin = block.position
        position = block.move(vector)
        remaining = block
        if type(self.grid[position]) is objects.Hole:
            remaining = self.fillHole(block, self.grid[position])
        if type(self.grid[position]) is objects.Block:
            remaining = self.stackBlocks(block, self.grid[position])
        self.grid[position] = remaining
        self.grid[origin] = None

    def fillHole(self, block, hole):
        if hole.size > block.size: #hole remains
            hole.size -= block.size
            self.blocks.remove(block)
            return hole
        elif hole.size < block.size: #block remains
            block.size -= hole.size
            self.holes.remove(hole)
            return block
        else: #neither remains
            self.blocks.remove(block)
            self.holes.remove(hole)
            return None

    def stackBlocks(self, block1, block2):
        block1.size += block2.size
        self.blocks.remove(block2)
        return block1
    
    def filterValue(self, value, position):
        if value == ' ':
            return
        elif value == '#':
            self.walls.append(objects.Wall(position))
            self.grid[position] = self.walls[-1]
        elif value == 'P':
            self.player = objects.Player(position)
            self.grid[position] = self.player
        elif value.islower():
            self.holes.append(objects.Hole(position, value))
            self.grid[position] = self.holes[-1]
        elif value.isupper():
            self.blocks.append(objects.Block(position, value))
            self.grid[position] = self.blocks[-1]
        else:
            raise ValueError(f'Format character "{value}" not recognized.')

class Game:
    def __init__(self, gameState, actionFunction):
        self.gameState = gameState
        self.actionFunction = actionFunction

    def run(self):
        print(self.gameState)
        while self.gameState.holes:
            print('Action: ', end = ' ')
            action = self.actionFunction(self.gameState)
            self.gameState.move(action)
            print(self.gameState)
        print('Leveled off.')
        return True

    @staticmethod
    def actionFromPlayer(*args):
        action = input().lower()
        if action not in ('w', 'a', 's', 'd', 'pw', 'pa', 'ps', 'pd'):
            print(f'"{action}" is not a valid action. Action: ', end = ' ')
            return Game.actionFromPlayer()
        mp = {'w':'NORTH', 'a':'WEST', 's':'SOUTH', 'd':'EAST'}
        prefix = 'PULL_' if action.startswith('p') else 'PUSH_'
        return prefix + mp[action[-1]]
