from random import sample, choice, random

from utils.snake import Snake

WALL = 1.0
MYHEAD = 0.0
# adders & mutipliers
# (value + value_a) * value_m
HUNGER_a = -101
HUNGER_m = 0.01
SNAKE_m = 0.01


class Game:
    
    def __init__(self, height, width, snake_cnt):
        
        # standard starting board positions (in order) for 7x7, 11x11, and 19x19
        # battlesnake uses random positions for any non-standard board size
        # https://github.com/BattlesnakeOfficial/engine/blob/master/rules/create.go
        positions = sample(
            [
                (1, 1), (height - 2, width - 2), (height - 2, 1), (1, width - 2),
                (1, width//2), (height//2, width - 2), (height - 2, width//2), (height//2, 1)
            ],
            snake_cnt)
        
        # I changed the data structure to speed up the game
        # empty_positions is used to generate food randomly
        self.empty_positions = {(y, x) for y in range(height) for x in range(width)}
        
        self.height = height
        self.width = width
        self.snake_cnt = snake_cnt
        
        self.snakes = [Snake(ID, 100, [positions[ID]] * 3) for ID in range(snake_cnt)]
        for snake in self.snakes:
            self.empty_positions.remove(snake.body[0])
        
        self.food = set(sample(self.empty_positions, snake_cnt))
        for food in self.food:
            self.empty_positions.remove(food)
        
        # two board sets are used to reduce run time
        self.heads = {snake.body[0]: {snake} for snake in self.snakes}
        self.bodies = {snake.body[i] for snake in self.snakes for i in range(1, len(snake.body))}
    # game rules
    # https://github.com/BattlesnakeOfficial/rules/blob/master/standard.go
    # this link below is what they use for the engine
    # they have defferent algorithms, resulting in different rules
    # https://github.com/BattlesnakeOfficial/engine/blob/master/rules/tick.go
    # I am using the online version (first one)
    def run(self, Alice, Bob=None, sep=None):
        if Bob:
            snake_ids1 = list(range(sep))
            snake_ids2 = list(range(sep, self.snake_cnt))
        else:
            snake_ids = list(range(self.snake_cnt))
        
        snakes = self.snakes
        # game procedures
        while len(snakes) > 1:
            
            # ask for moves
            if Bob:
                # one set might be empty
                # in that case the team with any snakes left wins
                if len(snake_ids1) == 0:
                    return snake_ids2[0]
                if len(snake_ids2) == 0:
                    return snake_ids1[0]
                states1 = [self.make_state(snake) for snake in snakes if snake.id < sep]
                states2 = [self.make_state(snake) for snake in snakes if snake.id >= sep]
                moves1 = Alice.make_moves(states1, snake_ids1)
                moves2 = Bob.make_moves(states2, snake_ids2)
                i = 0
                j = 0
            else:
                states = [self.make_state(snake) for snake in snakes]
                moves = Alice.make_moves(states, snake_ids)
                i = 0
            
            # execute moves
            for snake in snakes:
                if Bob:
                    if snake.id < sep:
                        new_head, old_head, tail = snake.move(moves1[i])
                        i += 1
                    else:
                        new_head, old_head, tail = snake.move(moves2[j])
                        j += 1
                else:
                    new_head, old_head, tail = snake.move(moves[i])
                    i += 1
                # update board sets
                try:
                    # several heads might come to the same cell
                    self.heads[new_head].add(snake)
                except KeyError:
                    self.heads[new_head] = {snake}
                    # if it goes into an empty cell
                    if new_head in self.empty_positions:
                        self.empty_positions.remove(new_head)
                if len(self.heads[old_head]) == 1:
                    del self.heads[old_head]
                else:
                    self.heads[old_head].remove(snake)
                self.bodies.add(old_head)
                if tail:
                    self.bodies.remove(tail)
                    self.empty_positions.add(tail)
            
            # reduce health
            for snake in snakes:
                snake.health -= 1
            
            # remove dead snakes
            # I have checked the code of the battlesnake game
            # their algorithm for checking collisions is shit
            # they run a nested for loop for every snake
            # this whole check through runs in O(n) time
            kills = set()
            for snake in snakes:
                head = snake.body[0]
                # check for wall collisions
                if head[0] < 0 or head[0] >= self.height or head[1] < 0 or head[1] >= self.width:
                    kills.add(snake)
                # check for body collisions
                elif head in self.bodies:
                    kills.add(snake)
                # check for head on collisions
                elif len(self.heads[head]) > 1:
                    for s in self.heads[head]:
                        if len(snake.body) <= len(s.body) and s != snake:
                            kills.add(snake)
                            break
                # check for starvation
                elif snake.health <= 0:
                    kills.add(snake)
            # remove from snakes set
            for snake in kills:
                # update board sets
                head = snake.body[0]
                if len(self.heads[head]) == 1:
                    del self.heads[head]
                    # it might die due to starvation or equal-length head on collision
                    # only in those two cases, the head position should become an empty space
                    # not out of bound and not into a body and not into a food
                    if head[0] >= 0 and head[0] < self.height and head[1] >= 0 and head[1] < self.width:
                        # head is in range
                        if head not in self.bodies and head not in self.food:
                            self.empty_positions.add(head)
                else:
                    self.heads[head].remove(snake)
                for i in range(1, len(snake.body)):
                    b = snake.body[i]
                    # it is possible that a snake has eaten on its first move and then die on its second move
                    # in that case the snake will have a repeated tail
                    # removing it from bodies twice causes an error
                    # tried to debug this one for 5 hours and finally got it
                    try:
                        self.bodies.remove(b)
                        self.empty_positions.add(b)
                    except KeyError:
                        pass
                snakes.remove(snake)
                if Bob:
                    if snake.id < sep:
                        snake_ids1.remove(snake.id)
                    else:
                        snake_ids2.remove(snake.id)
                else:
                    snake_ids.remove(snake.id)
            
            # check for food eaten
            for snake in snakes:
                if snake.body[0] in self.food:
                    food = snake.body[0]
                    self.food.remove(food)
                    snake.health = 100
                    snake.grow()
            
            # spawn food
            if len(self.food) == 0:
                chance = 1.0
            else:
                chance = 0.15
            if random() <= chance:
                try:
                    food = choice(tuple(self.empty_positions))
                    self.food.add(food)
                    self.empty_positions.remove(food)
                except IndexError:
                    # Cannot choose from an empty set
                    pass
        
        # return the winner if there is one
        return tuple(snakes)[0].id if snakes else None
    
    def make_state(self, you):
        """ Process the data and translate them into a grid
        
        Args:
            you: a Snake object define by snake.py; represents this snake
        
        Return:
            grid: a grid that represents the game
        
        """
        
        # gotta do the math to recenter the grid
        width = self.width * 2 - 1
        height = self.height * 2 - 1
        grid = [[WALL] * width for row in range(height)]
        center = (width//2, height//2)
        # the original game board
        # it's easier to work on the original board then transfer it onto the grid
        board = [[0] * self.width for row in range(self.height)]
        
        # positions are (y, x) not (x, y)
        # because you read the grid row by row, i.e. (row number, column number)
        # otherwise the board is transposed
        for food in self.food:
            # I suppose a food is more wanted than an enmpty cell so let EMPTY be the base value
            board[food[0]][food[1]] = (you.health + HUNGER_a) * HUNGER_m
        
        my_length = len(you.body)
        for snake in self.snakes:
            body = snake.body
            # get head
            board[body[0][0]][body[0][1]] = (len(body) - (my_length - 1)) * SNAKE_m
            # get the rest of the body
            dist = len(body)
            # Don't do the body[1:] slicing. It will copy the list
            for i in range(1, len(body)):
                board[body[i][0]][body[i][1]] = dist * SNAKE_m
                dist -= 1
        
        # get my head
        head = you.body[0]
        board[you.body[0][0]][you.body[0][1]] = MYHEAD
        
        # from this point, all positions are measured relative to our head
        for y in range(self.height):
            for x in range(self.width):
                grid[y - head[0] + center[1]][x - head[1] + center[0]] = board[y][x]
        
        return grid