from utils import Levels

class Wall:
    def __init__(self, position):
        self.position = position
        self.moveable = False

class Block:
    def __init__(self, position, size):
        self.position = position
        self.size = Levels.from_string(size)
        self.moveable = True

    def move(self, vector):
        r, c = self.position
        dr, dc, p = vector
        self.position = r + dr, c + dc
        return self.position

class Hole:
    def __init__(self, position, size):
        self.position = position
        self.size = Levels.from_string(size)
        self.moveable = False

class Player:
    def __init__(self, position):
        self.position = position
        self.moveable = True

    def move(self, vector):
        r, c = self.position
        dr, dc, p = vector
        self.position = r + dr, c + dc
        return self.position