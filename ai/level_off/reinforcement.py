import numpy as np, pandas as pd
import search, agents
from game import Game
from utils import Actions
from collections import defaultdict
import tensorflow as tf
import random

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
        return 10000
    newMini, newMaxi = newMinMax
    bonus = (state[state < 0].sum() - newState[newState < 0].sum())
    blockToHole = (search.manhattanDistance(mini, maxi) - search.manhattanDistance(newMini, newMaxi))
    bordering = newState[newPos[0] - 1: newPos[0] + 2, newPos[1] - 1: newPos[1] + 2]
    borderingPoints = (bordering > 0).any()
    reward = 200 * bonus + 10 * blockToHole
    return max(0, reward) + borderingPoints - 1

def getModel(input_shape):
    state = tf.keras.layers.Input(shape = input_shape)
    hidden = tf.keras.layers.Conv2D(16, 3, activation = 'relu', padding = 'same')(state)
    hidden = tf.keras.layers.Conv2D(16, 3, activation = 'relu', padding = 'same')(hidden)
    hidden = tf.keras.layers.Conv2D(16, 3, activation = 'relu', padding = 'same')(hidden)
    #hidden = tf.keras.layers.Dropout(0.2)(hidden)
    hidden = tf.keras.layers.Flatten()(hidden)
    hidden = tf.keras.layers.Dense(32, activation = 'relu')(hidden)
    #hidden = tf.keras.layers.Dropout(0.2)(hidden)
    output = tf.keras.layers.Dense(8)(hidden)
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
                print(f'\rTrial {i}: epochs - {epochs}')

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
    def __init__(self, model,  alpha=0.1, gamma=0.6, epsilon=0.1,
                                    rewardFunction=getManhattanReward):
        self.model = model
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.rewardFunction = rewardFunction
        self.actions = sorted(Actions.ACTIONS.keys())
        self.memory = defaultdict(list)
        self.experience = 0

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

    def getAction(self, state, legal):
        predictions = self.model.predict(self.makeArray(state)[np.newaxis,...])[0]
        row = pd.Series(predictions, index = self.actions)[legal]
        return row.index[row.argmax()]

    def update(self, state, problem, legal):
        x = self.makeArray(state)
        
        nextStates = []
        nextRewards = []
        for action in self.actions:
            if action not in legal:
                nextStates.append(self.makeArray(state))
                nextRewards.append(-1)
                continue
            newState = problem.generateSuccessor(state, action)
            reward = self.rewardFunction(state, newState)
            nextStates.append(self.makeArray(newState))
            nextRewards.append(reward)
        nextStates.append(self.makeArray(state))
        qScores = self.model.predict(np.array(nextStates))
        nextQMax, qScores = qScores[:8].max(axis = 1), qScores[-1]
        y = np.array(nextRewards + self.gamma * nextQMax)
        y = qScores + self.alpha * (y - qScores)
        self.memory[problem.name].append((x, y))

        if self.experience % 10 == 0:
            x, y = [], []
            for _, mem in self.memory.items():
                partialX, partialY = zip(*random.sample(mem[-1000:], min(len(mem), 200)))
                x.extend(partialX), y.extend(partialY)
            order = np.random.permutation(len(x))
            x = np.array(x)[order]
            y = np.array(y)[order]
            self.model.train_on_batch(x, y)

    def fit(self, problem, trials = 100, verbose = True, limit = 100000):
        for i in range(trials):
            epochs = 0
            state = problem.getStartState()
            legal = self.getLegalActions(state)
            while not problem.isGoalState(state):
                print(f'\r{problem.name} Training... {epochs}', end = '')
                self.experience += 1
                self.update(state, problem, legal)

                if np.random.rand() < self.epsilon:
                    action = np.random.choice(legal)
                else:
                    action = self.getAction(state, legal)

                state = problem.generateSuccessor(state, action)
                legal = self.getLegalActions(state)

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