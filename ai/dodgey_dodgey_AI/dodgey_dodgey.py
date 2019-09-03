'''
Dodgey Dodgey game.
'''

import random

class ObstacleThingie:
    def __init__(self, axis, position, direction):
        self.axis = axis
        self.position = position
        self.direction = direction
        self.is_overlapping = False
        
    def __str__(self):
        return 'Obstacle at ' + str(self.position)
        
    def print_me(self):
        thingie = {'x': {'1': '>', '-1': '<'}, 'y': {'1': 'v', '-1': '^'}}
        return thingie[self.axis][self.direction]
    
    def overlap(self, obs_list):
        if self in obs_list:
            obs_list.remove(self)
        self.is_overlapping = self.position in [obs.position for obs in obs_list]
        return self.is_overlapping
    
    def set_direction(self, new_d):
        self.direction = new_d
        
    def set_axis(self, new_a):
        self.axis = new_a
    
    def move_obstacle(self):
        (x, y) = self.position
        self.position = (x + int(self.direction), y) if self.axis == 'x'\
            else (x, y + int(self.direction))
        
class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        
    def __repr__(self):
        return 'Player({},{})'.format(self.name, self.position)
        
    def print_me(self):
        return 'P'
        
    def set_position(self, new_pos):
        self.position = new_pos


class PlayerField:
    def __init__(self, player, dimension):
        self.player = player
        self.dimension = dimension
        self.obs_dim = self.dimension + 2
        self.grid = self.construct_grid()
        self.obstacles = []
        
    def __repr__(self):
        self.update_grid()
        field = ''
        for i in range(self.obs_dim):
            if i == 0 or i == self.obs_dim - 1:    
                field += ' '.join(self.grid[i]) + '\n'
                if i == 0:
                    field += ' +' + '-+' * self.dimension + ' \n'
            else:
                field += '|'.join(self.grid[i]) + '\n'
                field += ' +' + '-+' * self.dimension + ' \n'
        return field
        
    def construct_grid(self):
        grid = []
        for i in range(self.obs_dim):
            grid.append([])
            for j in range(self.obs_dim):
                grid[i].append(' ')
        return grid
        
    def update_grid(self):
        self.grid = self.construct_grid()
        self.grid[self.player.position[1]][self.player.position[0]] = self.player.print_me()
        for obs in self.obstacles:
            obs_pos = self.grid[obs.position[1]][obs.position[0]]
            if obs_pos == 'P' or obs_pos == 'O':
                self.grid[obs.position[1]][obs.position[0]] = 'O'
            elif obs_pos == obs.print_me():
                self.grid[obs.position[1]][obs.position[0]] = obs.print_me()
            elif obs.overlap(self.obstacles.copy()):
                self.grid[obs.position[1]][obs.position[0]] = 'X'
            else:
                self.grid[obs.position[1]][obs.position[0]] = obs.print_me()
    
    def move_player(self):
        (x, y) = self.player.position
        motion_dict = {'w': (x, y - 1), 's': (x, y + 1),\
                       'a': (x - 1, y), 'd': (x + 1, y)}
        border_dict = {'s': y < self.dimension, 'w': y > 1,\
                       'a': x > 1, 'd': x < self.dimension}
        motion = input('Make a move: ').lower()
        if motion in motion_dict and border_dict[motion]:
            self.player.set_position(motion_dict[motion])
            return True
        else:
            print('That is not a valid action.')
            return False
    
    def new_obstacle(self):
        axis = random.choice(['x', 'y'])
        direction = random.choice(['1', '-1'])
        index = random.randint(1, self.dimension)
        pos_dict = {'x': {'1': (0, index), '-1': (self.obs_dim - 1, index)},\
            'y': {'-1': (index, self.obs_dim - 1), '1': (index, 0)}}
        self.obstacles.append(ObstacleThingie(axis, pos_dict[axis][direction], direction))
        
    def move_obstacles(self):
        for obs in self.obstacles:
            obs.move_obstacle()
            if max(obs.position[1], obs.position[0]) > self.obs_dim - 1\
               or min(obs.position[1], obs.position[0]) < 0:
                self.obstacles.remove(obs)
                
    #Add ricochet functionality when two obstacles overlap
    def ricochet(self):
        for obs in self.obstacles:
            if obs.overlap(self.obstacles.copy()):
                axis = random.choice(['x', 'y'])
                direction = random.choice(['1', '-1'])
                obs.set_direction(direction)
                obs.set_axis(axis)
                
    def print_overlap(self):
        for obs in self.obstacles:
            if obs.overlap(self.obstacles.copy()):
                print(obs)
            
def read_high_scores(filename):
    highscores_dict = {}
    file = open(filename)
    for line in file:
        line = line.strip()
        if line[0] != '#':
            line = line.split(',')
            if int(line[0]) not in highscores_dict:
                highscores_dict[int(line[0])] = {}
            highscores_dict[int(line[0])][bool(line[1])] = (line[2], int(line[3]))
    file.close()
    return highscores_dict
    
def check_high_scores(highscores_dict, size, ricochet, new_score, name):
        if size not in highscores_dict:
            highscores_dict[size] = {}
        if ricochet not in highscores_dict[size] or highscores_dict[size][ricochet][1] < new_score:
            highscores_dict[size][ricochet] = (name, new_score)
            return True
        else:
            return False
            
def save_high_scores(highscores_dict, filename):
    file = open(filename, 'w')
    file.write('#size,ricochet,name,score\n')
    for size in highscores_dict:
        for ricochet in highscores_dict[size]:
            player = highscores_dict[size][ricochet]
            file.write(str(size) + ',' + str(ricochet) + ',' + player[0] + ',' + str(player[1]) + '\n')
    file.close()


        
#============================================================================
def main():
    FILENAME = 'dodgey_scores.csv'
    high_scores = read_high_scores('dodgey_scores.csv')
    name = input('Please enter your name: ')
    size = int(input('What size field would you like to play? '))
    ricochet_mode = True if input('Would you like to play ricochet mode? (y|n) ').lower().strip()\
        in ('y', 'yes') else False
    
    if size in high_scores and ricochet_mode in high_scores[size]:
        HIGHSCORE = high_scores[size][ricochet_mode]
    else:
        HIGHSCORE = False
    
    player = Player(name, (random.randint(1, size), random.randint(1, size)))
    map = PlayerField(player, size)
    counter = 0
    print(map)
    
    #Check looping condition
    while map.player.position not in [obs.position for obs in map.obstacles]:
        map.move_obstacles()
        if ricochet_mode:
            map.ricochet()
        while not map.move_player():
            continue
        counter += 1            
        for i in range(counter//20 + 1):
            map.new_obstacle()
        print(map)
        print('Turn:', counter)
    
    print('Oh no! You got hit!!!')
    print(player.name, 'lasted', counter, 'turns on a size', size, 'x', size, 'field!!!')
    
    if check_high_scores(high_scores, size, ricochet_mode, counter, name):
        print('Congratulations! You set the high score for a', size, 'x', size, 'field with',
            'ricochet!!!' if ricochet_mode else 'no ricochet!!!')
        if HIGHSCORE:
            print('The previous high score was', HIGHSCORE[1], 'set by', HIGHSCORE[0] + '.')
        save_high_scores(high_scores, FILENAME)
    
    else:
        print('The high score for a', size, 'x', size, 'field  with', 'ricochet' if ricochet_mode else 'no ricochet', 
            'is', high_scores[size][ricochet_mode][1], 'by', high_scores[size][ricochet_mode][0] + '.')
        save_high_scores(high_scores, FILENAME)

if __name__ == '__main__':
    main()






















