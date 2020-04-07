import numpy as np, pandas as pd
import search, agents
from utils import Actions
from collections import defaultdict

def convertState(state):
    pos, state = state
    state = np.array(state)
    state[pos] = 999
    mod = np.array([v for v in state.flatten() if v is not None])
    pos = mod.argmax()
    mod[pos] = 0
    return pos, mod

def combinator(*args):
    if len(args) == 2:
        first, second = args
        states = []
        for elem1 in first:
            for elem2 in second:
                res = str(elem1) + str(elem2)
                states.append(res)
        return states
    return combinator(args[0], combinator(*args[1:]))

def getQState(state):
    pos, state = convertState(state)
    return str(pos) + ':' + ','.join(map(str, tuple(state)))

def getAllQStates(startState):
    #DEPRECATED
    pos, state = convertState(startState)
    maxBlock, minHole = state[state > 0].sum(), state[state < 0].min()
    positions = np.arange(len(state))
    args = [positions]
    for _ in positions:
        args.append(list(range(minHole, maxBlock + 1)))
    return combinator(*args)

def getReward(state, newState):
    #DEPRECATED
    #reward for filling holes
    #reward for pushing blocks, slightly less for pulling?
    #Walls won't move, so state and newState should have same length
    (pos, state), (newPos, newState) = convertState(state), convertState(newState)
    stateHoleTotal = state[state < 0].sum()
    newStateHoleTotal = newState[newState < 0].sum()
    if stateHoleTotal < newStateHoleTotal: #holes filled
        return newStateHoleTotal - stateHoleTotal
    #else: no holes filled, check for moved blocks
    differences = (newState - state)
    if (differences != 0).any():
        return 0.5
    return 0

def getMinMax(array):
    nonZeroPos = list(zip(*np.nonzero(array)))
    positions = {pos: array[pos] for pos in nonZeroPos}
    if not positions:
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
    posToBlock = search.manhattanDistance(pos, maxi) - search.manhattanDistance(newPos, newMaxi)
    blockToHole = search.manhattanDistance(mini, maxi) - search.manhattanDistance(newMini, newMaxi)
    return 1 + posToBlock + blockToHole + 1 * (differences != 0).any()

def buildQTable(startState):
    #DEPRECATED
    allStates = getAllQStates(startState)
    actions = Actions.ACTIONS.keys()
    table = pd.DataFrame(0, index = allStates, columns = actions)
    pd.to_pickle(table, 'qtable_scene1.pkl')
    return table

def qLearning(problem, alpha=0.1, gamma=0.6, epsilon=0.1, trials=1000, qTable = None):
    startState = problem.getStartState()
    actions = sorted(Actions.ACTIONS.keys())
    qTable = defaultdict(lambda: pd.Series(0, index = actions, dtype = float))
    for i in range(trials):
        epochs = 0
        state = startState
        qState = getQState(state)
        legal = agents.LegalAgent.getLegalActions(state)
        while not problem.isGoalState(state):
            if np.random.rand() < epsilon:
                action = np.random.choice(legal)
            else:
                action = legal[qTable[qState][legal].argmax()]

            newState = problem.generateSuccessor(state, action)
            newQState = getQState(newState)
            newLegal = agents.LegalAgent.getLegalActions(newState)

            qValue = qTable[qState][action]
            #reward = getReward(state, newState)
            reward = getManhattanReward(state, newState)
            nextMax = qTable[newQState][newLegal].max()

            newQValue = (1 - alpha) * qValue + alpha * (reward + gamma * nextMax)
            qTable[qState][action] = newQValue

            state, qState, legal = newState, newQState, newLegal
            epochs += 1
            #if epochs % 100 == 0:
             #   print(state)

        if i % 1 == 0:
            print(f'Trial {i}: epochs - {epochs}')
    
    return qTable

def qSearch(problem, qTable):
    startState = problem.getStartState()
    state = startState
    qState = getQState(state)
    path = []
    while not problem.isGoalState(state):
        legal = agents.LegalAgent.getLegalActions(state)
        action = legal[qTable[qState][legal].argmax()]
        path.append(action)

        newState = problem.generateSuccessor(state, action)
        newQState = getQState(newState)

        state, qState = newState, newQState
    return path

def qInference(qTable):

    def infer(problem):
        return qSearch(problem, qTable)

    return infer