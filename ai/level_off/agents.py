from utils import Actions

class LegalAgent:
    
    @staticmethod
    def getLegalActions(state):
        actions = []
        for direction, vector in Actions.ACTIONS.items():
            checker = LegalAgent.legalPush if vector[-1] > 0 else LegalAgent.legalPull
            if checker(vector, state):
                actions.append((direction, vector))
        return actions

    @staticmethod
    def legalPush(vector, state):
        dr, dc, p = vector
        position, grid = state
        r, c = position
        if not LegalAgent.legalPosition((r + dr, c + dc), grid):
            return False
        if grid[r + dr][c + dc] is None:
            return False #can't push a wall
        elif grid[r + dr][c + dc] < 0:
            return False #can't push a hole
        elif grid[r + dr][c + dc] == 0:
            return True
        else:
            return LegalAgent.legalBlockPush(vector, (r + dr, c + dc), state)

    @staticmethod
    def legalPull(vector, state):
        dr, dc, p = vector
        position, grid = state
        r, c = position
        if not LegalAgent.legalPosition((r + dr, c + dc), grid):
            return False
        if not LegalAgent.legalPosition((r - dr, c - dc), grid):
            return False
        if grid[r - dr][c - dc] is None:
            return False #can't pull a wall
        elif grid[r - dr][c - dc] <= 0:
            return False #can't pull a hole or empty space
        if grid[r + dr][c + dc] is None:
            return False #can't move into a wall
        elif grid[r + dr][c + dc] > 0:
            return False #can't move into a block
        else:
            return LegalAgent.legalPush(vector, state)

    @staticmethod
    def legalBlockPush(vector, position, state):
        dr, dc, p = vector
        r, c = position
        grid = state[1]
        if not LegalAgent.legalPosition((r + dr, c + dc), grid):
            return False
        if grid[r + dr][c + dc] is None:
            return False
        return True
        
    @staticmethod
    def legalPosition(position, grid):
        r, c = position
        try:
            grid[r][c]
        except IndexError:
            return False
        return True
            

        