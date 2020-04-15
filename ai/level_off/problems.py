from agents import LegalAgent
from utils import Actions
from game import GameState
import os, random

class LevelProblem:
    def __init__(self, gameState, name = ''):
        self.gameState = gameState
        self.start = (gameState.getPlayerPosition(), gameState.getState())
        self.walls = gameState.getWalls()
        self.expanded = 0
        self.name = name
    
    def __hash__(self):
        return hash(self.name)

    def getStartState(self):
        return self.start

    def getGameState(self):
        return self.gameState

    def isGoalState(self, state):
        grid = state[1]
        blocks = lambda x: x is not None and x > 0
        holes = lambda x: x is not None and x < 0
        gridChecker = lambda grid, check: any([any(map(check, row)) for row in grid])
        return not (gridChecker(grid, blocks) and gridChecker(grid, holes))

    def getSuccessors(self, state):
        successors = []
        self.expanded += 1
        for direction in LegalAgent.getLegalActions(state):
            newState = self.generateSuccessor(state, direction)
            cost = 1
            successors.append((newState, direction, cost))
        return successors

    def getName(self):
        return self.name

    @staticmethod
    def generateSuccessor(state, direction):
        position, grid = state
        r, c = position
        dr, dc, p = Actions.ACTIONS[direction]
        editable = list(map(list, grid))
        if p < 0: #pull
            editable[r][c] += editable[r - dr][c - dc]
            editable[r - dr][c - dc] = 0
        else: #push
            if editable[r + 2*dr][c + 2*dc] is not None:
                editable[r + 2*dr][c + 2*dc] += editable[r + dr][c + dc]
                editable[r + dr][c + dc] = 0
        newState = ((r + dr, c + dc), tuple(map(tuple, editable)))
        return newState

    @classmethod
    def fromFile(cls, fname):
        gameState = GameState.fromFile(fname)
        return cls(gameState, name = fname)

class ProblemSet:
    def __init__(self, problems = []):
        self.problems = list(problems)

    def __iter__(self):
        return iter(self.problems)

    def addProblem(self, problem):
        self.problems.append(problem)

    def randomProblem(self):
        return random.choice(self.problems)

    @classmethod
    def fromDirectory(cls, directory):
        problems = []
        for file in os.listdir(directory):
            if file.endswith('.results'):
                continue
            problem = LevelProblem.fromFile(directory + '/' + file)
            problems.append(problem)
        return cls(problems)
            
