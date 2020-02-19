from utils import Actions
import objects

class Agent:
    def __init__(self, gameState):
        self.grid = gameState.getGrid()
        self.player = gameState.getPlayer()

    def getLegalActions(self):
        actions = []
        for direction, vector in Actions.ACTIONS.items():
            checker = self.legalPush if vector[-1] > 0 else self.legalPull
            if checker(vector):
                actions.append(direction)
        return actions

    def legalPush(self, vector):
        dr, dc, p = vector
        r, c = self.player.position
        if type(self.grid[r + dr, c + dc]) in (objects.Wall, objects.Hole):
            return False
        elif self.grid[r + dr, c + dc] is None:
            return True
        else:
            return self.legalBlockPush((r + dr, c + dc), vector)

    def legalPull(self, vector):
        dr, dc, p = vector
        r, c = self.player.position
        if type(self.grid[r - dr, c - dc]) is objects.Block:
            if type(self.grid[r + dr, c + dc]) is not objects.Block:
                return self.legalPush((-dr, -dc, p))
        return False

    def legalBlockPush(self, position, vector):
        dr, dc, p = vector
        r, c = position
        if type(self.grid[r + dr, c + dc]) is objects.Wall:
            return False
        return True
        
            

        