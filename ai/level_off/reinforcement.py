import numpy as np, pandas as pd
import search, agents
from game import Game
from utils import Actions
from collections import defaultdict
import tensorflow as tf
from scipy.special import softmax

def getMinMax(array):
    nonZeroPos = list(zip(*np.nonzero(array)))
    positions = {pos: array[pos] for pos in nonZeroPos}
    if not positions or (array >= 0).all() or (array <= 0).all():
        return 0
    mini = min(positions, key = lambda x: positions[x])
    maxi = max(positions, key = lambda x: positions[x])
    return mini, maxi

def fillNone(array, value = 0):
    rows, cols = array.shape
    for i in range(rows):
        for j in range(cols):
            if array[i, j] is None:
                array[i, j] = value

def getManhattanReward(state, newState):
    pos, state = state[0], np.array(state[1])
    newPos, newState = newState[0], np.array(newState[1])
    fillNone(state), fillNone(newState)
    differences = (newState - state)
    mini, maxi = getMinMax(state)
    newMinMax = getMinMax(newState)
    if newMinMax == 0:
        return 100
    newMini, newMaxi = newMinMax
    bonus = 50 * (state[state < 0].sum() < newState[newState < 0].sum())
    posToBlock = search.manhattanDistance(pos, maxi) - search.manhattanDistance(newPos, newMaxi)
    blockToHole = search.manhattanDistance(mini, maxi) - search.manhattanDistance(newMini, newMaxi)
    return bonus + 1 + posToBlock + blockToHole + 1 * (differences != 0).any()

def getModel(input_shape):
    state = tf.keras.layers.Input(shape = input_shape)
    hidden = tf.keras.layers.Conv2D(8, 3, activation = 'relu')(state)
    hidden = tf.keras.layers.Conv2D(8, 3, activation = 'relu')(hidden)
    hidden = tf.keras.layers.Conv2D(8, 3, activation = 'relu')(hidden)
    hidden = tf.keras.layers.Flatten()(hidden)
    #output = tf.keras.layers.Dense(8, activation = 'relu')(hidden)
    output = tf.keras.layers.Dense(8, activation = 'softmax')(hidden)
    return tf.keras.models.Model(state, output)

class QAgent:
    def __init__(self, alpha=0.1, gamma=0.6, epsilon=0.1,
                            rewardFunction=getManhattanReward):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.rewardFunction = rewardFunction
        actions = sorted(Actions.ACTIONS.keys())
        self.qTable = defaultdict(lambda: pd.Series(0.0, index = actions))

    def getLegalActions(self, state):
        return agents.LegalAgent.getLegalActions(state)

    def getAction(self, state, legal):
        row = self.qTable[state][legal]
        return np.random.choice(row[row == row.max()].index)

    def update(self, state, newState, reward, newLegal, action):
        qValue = self.qTable[state][action]
        nextMax = self.qTable[newState][newLegal].max()

        newQValue = (1 - self.alpha) * qValue
        newQValue += self.alpha * (reward + self.gamma * nextMax)
        self.qTable[state][action] = newQValue

    def fit(self, problem, trials = 100, verbose = True):
        for i in range(trials):
            epochs = 0
            state = problem.getStartState()
            legal = self.getLegalActions(state)
            while not problem.isGoalState(state):
                print(f'\rTraining... {epochs}', end = '')
                if np.random.rand() < self.epsilon:
                    action = np.random.choice(legal)
                else:
                    action = self.getAction(state, legal)

                newState = problem.generateSuccessor(state, action)
                newLegal = self.getLegalActions(newState)
                reward = self.rewardFunction(state, newState)

                self.update(state, newState, reward, newLegal, action)

                state, legal = newState, newLegal
                epochs += 1

            if verbose and i % 1 == 0:
                print(f'Trial {i}: epochs - {epochs}')

    def search(self, problem):
        state = problem.getStartState()
        path = []
        while not problem.isGoalState(state):
            legal = agents.LegalAgent.getLegalActions(state)
            action = self.getAction(state, legal)
            path.append(action)

            newState = problem.generateSuccessor(state, action)
            state = newState

        return path

class DeepQAgent:
    def __init__(self, model,  alpha=0.1, gamma=0.6, epsilon=0.1, beta = 0.5,
                                    rewardFunction=getManhattanReward):
        self.model = model
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.beta = beta
        self.rewardFunction = rewardFunction
        self.actions = sorted(Actions.ACTIONS.keys())
        self.qTable = defaultdict(lambda: pd.Series(0.0, index = self.actions))
        self.memory = []

    def getLegalActions(self, state):
        return agents.LegalAgent.getLegalActions(state)

    def makeArray(self, state):
        pos, state = state
        array = np.zeros((len(state), len(state[0]), 4))
        state = np.array(state)
        array[pos[0], pos[1], 0] = 1
        array[state == None, 1] = 1
        fillNone(state)
        array[state < 0, 2] = state[state < 0]
        array[state > 0, 3] = state[state > 0]
        return array

    def getAction(self, state, legal, qTable = False):
        if qTable:
            row = self.qTable[state][legal]
            return np.random.choice(row[row == row.max()].index)
        predictions = self.model.predict(self.makeArray(state)[np.newaxis,...])[0]
        row = pd.Series(predictions, index = self.actions)[legal]
        return np.random.choice(row[row == row.max()].index)

    def update(self, state, problem, legal):
        x = self.makeArray(state)
        y = []
        for action in self.actions:
            if action not in legal:
                y.append(0)
                continue
            newState = problem.generateSuccessor(state, action)
            reward = self.rewardFunction(state, newState)
            newLegal = self.getLegalActions(newState)
            self.updateQTable(state, newState, reward, newLegal, action)
        #y = np.array(y)
        y = softmax(self.qTable[state])
        self.memory.append((x, y))

        if len(self.memory) % 64 == 0:
            x, y = zip(*self.memory[-64:])
            self.model.train_on_batch(np.array(x), np.array(y))

    def updateQTable(self, state, newState, reward, newLegal, action):
        qValue = self.qTable[state][action]
        nextMax = self.qTable[newState][newLegal].max()

        newQValue = (1 - self.alpha) * qValue
        newQValue += self.alpha * (reward + self.gamma * nextMax)
        self.qTable[state][action] = newQValue

    def fit(self, problem, trials = 100, verbose = True, limit = 10000):
        for i in range(trials):
            epochs = 0
            state = problem.getStartState()
            legal = self.getLegalActions(state)
            while not problem.isGoalState(state):
                print(f'\r{problem.name} Training... {epochs}', end = '')
                self.update(state, problem, legal)
                
                if np.random.rand() < self.epsilon:
                    action = np.random.choice(legal)
                else:
                    action = self.getAction(state, legal, qTable = not np.random.binomial(1, self.beta))

                newState = problem.generateSuccessor(state, action)
                newLegal = self.getLegalActions(newState)

                state, legal = newState, newLegal
                epochs += 1

                if epochs >= limit:
                    break

            if verbose:
                print(f'\rTrial {i}: epochs - {epochs}')

        return epochs

    def fitProblemSet(self, problemSet, trials = 100, verbose = True):
        for i in range(trials):
            problem = problemSet.randomProblem()
            print(f'\r{problem.name} Training...', end = '')
            epochs = self.fit(problem, trials=1, verbose=False)
            if verbose:
                print(f'\rTrial {i}: {problem.name} epochs - {epochs}')

    def search(self, problem, limit = 500):
        state = problem.getStartState()
        path = []
        while not problem.isGoalState(state):
            legal = agents.LegalAgent.getLegalActions(state)
            action = self.getAction(state, legal)
            path.append(action)

            newState = problem.generateSuccessor(state, action)
            state = newState

            if len(path) >= limit:
                return path
        return path

    def searchAll(self, problemSet, limit = 500, record = None, verbose = True):
        for problem in problemSet:
            solution = self.search(problem, limit = limit)
            if verbose:
                print(f'{problem.name}: path length - {len(solution)}')
            playing = Game(problem.getGameState(), Game.actionFromList(solution))
            if record:
                with open(problem.name + '.results', 'w') as fp:
                    playing.run(pause=0.0, file = fp)

    def save(self, filepath):
        self.model.save_weights(filepath)