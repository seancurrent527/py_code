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
                  Directions.WEST : (0, -1)}

    # -1 pull, 1 push
    ACTIONS = {'PUSH_' + key: value + (1,) for key, value in DIRECTIONS.items()}
    ACTIONS.update({'PULL_' + key: value + (-1,) for key, value in DIRECTIONS.items()})

class Levels:
    LETTERS = 'ABCDEFGHIJKLMN'
    SIZES = {'ABCDEFGHIJKLMN'[i]: i + 1 for i in range(len('ABCDEFGHIJKLMN'))}
    SIZES.update({k.lower(): -v for k, v in SIZES.items()})
    SYMBOLS = {v: k for k, v in SIZES.items()}

    @staticmethod
    def from_string(size):
        return Levels.SIZES[size]