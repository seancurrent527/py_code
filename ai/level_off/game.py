import objects
from utils import Actions, Levels
import numpy as np
import time

class GameState:
    def __init__(self, formatString):
        self.blocks = []
        self.holes = []
        self.walls = []
        grid = formatString.split('\n')
        r = len(grid)
        c = len(grid[0])
        self.size = (r, c)
        self.grid = np.full(self.size, None, dtype=object)
        for i in range(r):
            for j in range(c):
                self.filterValue(grid[i][j], (i, j))
        self.grid[self.getPlayerPosition()] = self.player

    def __str__(self):
        stringList = []
        for row in self.grid:
            stringList.append([])
            for item in row:
                if type(item) is objects.Wall:
                    stringList[-1].append('#')
                elif item is None:
                    stringList[-1].append(' ')
                elif type(item) is objects.Player:
                    stringList[-1].append('P')
                else:
                    stringList[-1].append(Levels.SYMBOLS[item.size])
        return '\n'.join([''.join(ls) for ls in stringList])

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

    def getState(self):
        grid = np.zeros_like(self.grid, dtype = object)
        for block in self.blocks:
            grid[block.position] = block.size
        for hole in self.holes:
            grid[hole.position] = hole.size
        for wall in self.walls:
            grid[wall.position] = None
        return tuple(map(tuple, grid))

    def move(self, direction):
        try:
            vector = Actions.ACTIONS[direction]
        except KeyError:
            return False
        if vector[-1] > 0:
            return self.pushPlayer(vector)
        else:
            return self.pullPlayer(vector)

    def pushPlayer(self, vector):
        origin = self.player.position
        position = self.player.move(vector)
        if self.grid[position] is not None:
            if type(self.grid[position]) is not objects.Block:
                self.player.position = origin
                return False
            outcome = self.moveBlock(self.grid[position], vector)
            if not outcome:
                self.player.position = origin
                return False
        self.grid[position] = self.player
        self.grid[origin] = None
        return True

    def pullPlayer(self, vector):
        origin = self.player.position
        position = self.player.move(vector)
        pullPosition = origin[0] - vector[0], origin[1] - vector[1]
        if self.grid[position] is not None:
            self.player.position = origin
            return False
        if type(self.grid[pullPosition]) is objects.Block:
            self.moveBlock(self.grid[pullPosition], vector)
        else:
            self.grid[origin] = None
        self.grid[position] = self.player
        return True
        
    def moveBlock(self, block, vector):
        origin = block.position
        position = block.move(vector)
        remaining = block
        if type(self.grid[position]) is objects.Hole:
            remaining = self.fillHole(block, self.grid[position])
        elif type(self.grid[position]) is objects.Block:
            remaining = self.stackBlocks(block, self.grid[position])
        elif type(self.grid[position]) is objects.Wall:
            block.position = origin
            return False
        self.grid[position] = remaining
        self.grid[origin] = None
        return True

    def fillHole(self, block, hole):
        difference = hole.size + block.size
        if difference < 0: #hole remains
            hole.size += block.size
            self.blocks.remove(block)
            return hole
        elif difference > 0: #block remains
            block.size += hole.size
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

    def run(self, pause = 0):
        print(self.gameState)
        cost = 0
        while self.gameState.holes and self.gameState.blocks:
            print('Action: ', end = ' ')
            action = self.actionFunction()
            cost += 1
            result = self.gameState.move(action)
            print()
            if not result:
                cost -= 1
                print('That is not a valid action.')
            print(self.gameState)
            time.sleep(pause)
        print('Leveled off.')
        print('Cost: ', cost)
        return True

    @staticmethod
    def actionFromPlayer():
        
        def getAction():
            action = input().lower()
            if action not in ('w', 'a', 's', 'd', 'pw', 'pa', 'ps', 'pd'):
                print(f'"{action}" is not a valid action. Action: ', end = ' ')
                return Game.actionFromPlayer()
            mp = {'w':'NORTH', 'a':'WEST', 's':'SOUTH', 'd':'EAST'}
            prefix = 'PULL_' if action.startswith('p') else 'PUSH_'
            return prefix + mp[action[-1]]

        return getAction

    @staticmethod
    def actionFromList(ls):
        
        def getAction():
            action = ls[0]
            del ls[0]
            return action

        return getAction
