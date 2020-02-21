from agents import LegalAgent

class LevelProblem:
    def __init__(self, gameState):
        self.startingGameState = gameState
        self.start = (gameState.getPlayerPosition(), gameState.getState())
        self.walls = gameState.getWalls()
    
    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        grid = state[1]
        blocks = lambda x: x is not None and x > 0
        holes = lambda x: x is not None and x < 0
        gridChecker = lambda grid, check: any([any(map(check, row)) for row in grid])
        return not (gridChecker(grid, blocks) and gridChecker(grid, holes))

    def getSuccessors(self, state):
        successors = []
        for direction, vector in LegalAgent.getLegalActions(state):
            position, grid = state
            r, c = position
            dr, dc, p = vector 
            editable = list(map(list, grid))
            if p < 0: #pull
                editable[r][c] += editable[r - dr][c - dc]
                editable[r - dr][c - dc] = 0
            else: #push
                if editable[r + 2*dr][c + 2*dc] is not None:
                    editable[r + 2*dr][c + 2*dc] += editable[r + dr][c + dc]
                    editable[r + dr][c + dc] = 0
            newState = ((r + dr, c + dc), tuple(map(tuple, editable)))
            cost = 1
            successors.append((newState, direction, cost))
        return successors