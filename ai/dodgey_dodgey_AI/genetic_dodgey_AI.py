'''
AI for dodgey_dodgey.
'''

import numpy as np, random, time
import dodgey_dodgey_framework as ddf
import genetic_framework as gf


#Rate the AI by how "safe" it is: ie, tree looks forward 3-4 turns, assigns a threat to each outcome
#Genetic algorithm, regresses on underlying grid

def manhattan_distance(x1,y1,x2,y2):
    return abs(x1-x2) + abs(y1-y2)

def print_char(x):
            if (x == np.array([0,0,0,0,1])).all():
                return 'P'
            if sum(x) == 0:
                return ' '
            if x[-1] == 1 and sum(x) >= 2:
                return 'O'
            if sum(x) >= 2:
                return 'X'
            else:
                return 'v^><'[x.argmax()]

def construct_subgrid(grid, view = 2):
    y, x = list(zip(*np.where(grid[...,-1] == 1)))[0]
    base = np.zeros((2*view + 1, 2*view + 1,5))
    sub = grid[max(0,y-view):y+view+1, max(0,x-view):x+view+1,:]
    ypos, xpos = list(zip(*np.where(sub[...,-1] == 1)))[0]
    #should only use ypos and xpos
    lower_y, lower_x = max(0, view - ypos), max(0, view - xpos)
    upper_y, upper_x = lower_y + sub.shape[0], lower_x + sub.shape[1]
    base[lower_y:upper_y, lower_x:upper_x,:] = sub
    '''
    try: base[lower_y:upper_y, lower_x:upper_x,:] = sub
    except ValueError:
        print(base[lower_y:upper_y, lower_x:upper_x,:],sub, sep = '\n')
        raise ValueError
    '''
    return base

def sum_around(y, x, grid):
    directions = [(0,0),(0,1),(0,-1),(1,0),(-1,0)]
    total = 0
    for d in directions:
        try:
            total += grid[y+d[0], x+d[1]] 
        except IndexError:
            continue
    return total

def star_sum(y, x, grid, stars = 2, weights = None):
    directions = [(0,1),(0,-1),(1,0),(-1,0)]
    if weights is None:
        weights = [1] * stars + 2
    if stars == 1:
        return weights[0] * sum_around(y, x, grid) 
    else:
        return weights[0] * sum(star_sum(y+d[0],x+d[1],grid,stars=stars-1, weights = weights[1:]) for d in directions)


#Create threat grid: for each arrow, add some value based off of decider coeffs to the locations in the direction of the arrow. 

'''
NOTE: AI ONLY HAS TO CALCULATE EVERY OTHER SPACE FOR DANGER! Arrows directly next to it do not have the ability to harm it.
'''

class DirectionalRegressor:
    def __init__(self, grid_size, mutation_rate = 0.1, stars = 2):
        self.coeffs = np.random.rand(grid_size) * 200 - 100
        self.grid_size = grid_size
        self.mutation_rate = mutation_rate
        self.stars = stars
        self.star_weights = np.random.rand(stars + 2) * 200 - 100 
        self.prev_pos = (0,0)
        self.curr_pos = (0,0)
        self.prev = '--'
        self.limit = 1

    def threat_grid(self, v_subgrid):
        threat = np.zeros(v_subgrid.shape[:-1])
        center = len(v_subgrid)//2; center = (center, center)
        transformer = np.array([[1,0],[-1,0],[0,1],[0,-1]])
        locations = lambda v, xy: [[tuple(transformer[k]*l + xy) for l in range(1, len(self.coeffs))] for k in range(4) if v[k] == 1]
        for i in range(len(v_subgrid[0])):
            for j in range(len(v_subgrid)):
                if manhattan_distance(i,j,*center) % 2 == 0 and sum(v_subgrid[j,i]) != 0:
                    locs = locations(v_subgrid[j,i], (j,i))
                    for row in locs:
                        for m in range(len(row)):
                            try:
                                threat[row[m]] += self.coeffs[m]
                            except IndexError:
                                break
        #print(threat)
        return threat

    def decider(self, board):   
        self.curr_pos = (board.player.y, board.player.x)
        threat = self.threat_grid(construct_subgrid(board.grid, view = self.stars))
        x = y = len(threat) // 2
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        moves = 'swda'
        levels = np.array([star_sum(y+d[1], x+d[0], threat,self.stars,
                 weights = self.star_weights[:-1]) for d in directions])
        #[print('v^><'[i],levels[i]) for i in range(4)]
        new = levels.argmin()
        while self.prev_pos == self.curr_pos and moves[new] in self.prev[self.limit:]:
                levels[new] = levels.max() + 1
                new = levels.argmin()
                self.limit -= 1
        self.prev_pos = self.curr_pos
        self.limit = 1
        self.prev = self.prev[-1] + moves[new]
        return moves[new]

    def mate(self, other):
        new = DirectionalRegressor(self.grid_size, self.mutation_rate, self.stars)
        if random.random() <= self.mutation_rate:
            return new
        else:
            new.coeffs = (self.coeffs + other.coeffs) / 2
            new.star_weights = (self.star_weights + other.star_weights) / 2
            return new

    def fitness(self, grid_size = 7):
        board = ddf.GameGrid(grid_size)
        return ddf.play_game(board, self.decider, printing = False)

#===================================================================================
def main():
    GRIDSIZE = 7
    fitness = lambda x: sum(DirectionalRegressor.fitness(x, GRIDSIZE) for i in range(30))/30
    algo = gf.Evolution(GRIDSIZE, fitness, DirectionalRegressor.mate, species=DirectionalRegressor)
    ls = []
    for i in range(20):
        prime, score = algo.evolve(30, 1, 0.5)
        ls.append(score)
        #time.sleep(5)
        ddf.play_game(ddf.GameGrid(GRIDSIZE), prime.decider, sleep = 0, printing = False)
        #time.sleep(15)
    print(ls)

if __name__ == '__main__':
    main()




