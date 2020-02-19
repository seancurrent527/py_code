class Directions:
    NORTH = 'NORTH'
    SOUTH = 'SOUTH'
    EAST = 'EAST'
    WEST = 'WEST'
    STOP = 'STOP'

class Actions:
    DIRECTIONS = {Directions.NORTH : (-1, 0),
                  Directions.SOUTH : (1, 0),
                  Directions.EAST : (0, 1),
                  Directions.WEST : (0, -1),
                  Directions.STOP : (0, 0)}

    # -1 pull, 1 push
    ACTIONS = {'PUSH_' + key: value + (1,) for key, value in DIRECTIONS.items()}
    ACTIONS.update({'PULL_' + key: value + (-1,) for key, value in ACTIONS.items()})

class Levels:
    sizes = {'A' : 1,
             'B' : 2,
             'C' : 3,
             'D' : 4,
             'E' : 5,
             'a' : -1,
             'b' : -2,
             'c' : -3,
             'd' : -4,
             'e' : -5}

    @staticmethod
    def from_string(size):
        return Levels.sizes[size]