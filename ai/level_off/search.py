import utils

#Simple class to create directed trees mapping child -> parent
class Branch:
    def __init__(self, state, action = None, cost = 0, heuristic = 0, parent = None):
        self.state = state
        self.action = action
        self.cost = cost
        self.heuristic = 0
        self.parent = parent

    def path(self):
        path = [] #add previous actions to path, then reverse
        branch = self
        while branch.action:
            path.append(branch.action)
            branch = branch.parent #move to parent branch
        return path[::-1]

def depthFirstSearch(problem):
    parseStack = utils.Stack()
    state = problem.getStartState()
    parseStack.push(Branch(state)) #push root branch to stack
    visited = set()
    while not parseStack.isEmpty():
        branch = parseStack.pop()
        if branch.state not in visited:
            visited.add(branch.state)
            if problem.isGoalState(branch.state):
                return branch.path()
            for state, action, _ in problem.getSuccessors(branch.state):    
                parseStack.push(Branch(state, action, parent = branch))

def breadthFirstSearch(problem):
    parseQ = utils.Queue()
    state = problem.getStartState()
    parseQ.push(Branch(state)) #push root branch to queue
    visited = set()
    while not parseQ.isEmpty():
        branch = parseQ.pop()
        if branch.state not in visited:
            visited.add(branch.state)
            if problem.isGoalState(branch.state):
                return branch.path()
            for state, action, _ in problem.getSuccessors(branch.state):    
                parseQ.push(Branch(state, action, parent = branch))

def uniformCostSearch(problem):
    parsePQ = utils.PriorityQueue()
    state = problem.getStartState()
    parsePQ.push(Branch(state), 0) #push root branch to queue with cost 0
    visited = set()
    while not parsePQ.isEmpty():
        branch = parsePQ.pop()
        if branch.state not in visited:
            visited.add(branch.state)
            if problem.isGoalState(branch.state):
                return branch.path()
            for state, action, cost in problem.getSuccessors(branch.state):    
                cost = cost + branch.cost
                parsePQ.push(Branch(state, action, cost = cost, parent = branch), cost)

def aStarSearch(problem, heuristic=lambda: 0):
    parsePQ = utils.PriorityQueue()
    state = problem.getStartState()
    parsePQ.push(Branch(state), 0) #push root branch to queue with cost 0
    visited = set()
    while not parsePQ.isEmpty():
        branch = parsePQ.pop()
        if branch.state not in visited:
            visited.add(branch.state)
            if problem.isGoalState(branch.state):
                return branch.path()
            for state, action, cost in problem.getSuccessors(branch.state):    
                cost = cost + branch.cost
                parsePQ.push(Branch(state, action, cost = cost, parent = branch), cost + heuristic(state, problem))

def aStar(heuristic):
    
    def aStarFunction(problem):
        return aStarSearch(problem, heuristic=heuristic)
    
    return aStarFunction

def manhattanDistance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])

def distanceHeuristic(state, problem):
    position, grid = state
    holes, blocks = [], []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] is not None:
                if grid[r][c] > 0:
                    blocks.append((r, c))
                elif grid[r][c] < 0:
                    holes.append((r, c))
    if not holes or not blocks:
        return 0
    nearestBlock = min(blocks, key = lambda x: manhattanDistance(position, x))
    nearestHole = min(holes, key = lambda x: manhattanDistance(nearestBlock, x))
    return manhattanDistance(position, nearestBlock) + manhattanDistance(nearestBlock, nearestHole)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch