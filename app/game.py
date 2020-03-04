from random import sample, choice, random

from snake import Snake

max_snakes = 8
EMPTY = 0.5
# adders & mutipliers
# (value + value_a) * value_m
HUNGER_a = -101
HUNGER_m = 0.005
SNAKE_m = 0.005

class Game:
    
    def __init__(self, height, width, snake_cnt):
        
        assert snake_cnt <= max_snakes
        
        # standard starting board positions (in order) for 7x7, 11x11, and 19x19
        # battlesnake uses random positions for any non-standard board size
        # https://github.com/BattlesnakeOfficial/engine/blob/master/rules/create.go
        positions = [
            (1, 1), (height - 2, width - 2), (height - 2, 1), (1, width - 2),
            (1, width//2), (height//2, width - 2), (height - 2, width//2), (height//2, 1)
        ]
        
        # I changed the data structure to speed up the game
        # empty_positions is used to generate food randomly
        self.empty_positions = {(y, x) for y in range(height) for x in range(width)}
        
        self.height = height
        self.width = width
        
        self.snakes = {Snake(ID, 100, [positions[ID]] * 3) for ID in range(snake_cnt)}
        for snake in self.snakes:
            self.empty_positions.remove(snake.body[0])
        
        self.food = set(sample(self.empty_positions, snake_cnt))
        for food in self.food:
            self.empty_positions.remove(food)
        
        # two board sets are used to reduce run time
        self.heads = {snake.body[0]: {snake} for snake in self.snakes}
        self.bodies = {snake.body[i] for snake in self.snakes for i in range(1, len(snake.body))}
        
        # the game stores the current state
        self.state = [[[EMPTY] * width for row in range(height)] for layer in range(max_snakes)]
        # make a state for each snake (just a reference list)
        self.states = [self.state.copy() for _ in range(snake_cnt)]
        for i in range(1, snake_cnt):
            temp = self.states[i][0]
            self.states[i][0] = self.states[i][i]
            self.states[i][i] = temp
        
        for snake in self.snakes:
            board = self.state[snake.id]
            dist = len(snake.body)
            for b in snake.body:
                board[b[0]][b[1]] += dist * SNAKE_m
                dist -= 1
            for food in self.food:
                board[food[0]][food[1]] = EMPTY + (snake.health + HUNGER_a) * HUNGER_m

    # game rules
    # https://github.com/BattlesnakeOfficial/rules/blob/master/standard.go
    # this link below is what they use for the engine
    # they have defferent algorithms, resulting in different rules
    # https://github.com/BattlesnakeOfficial/engine/blob/master/rules/tick.go
    # I am using the engine version (second one)
    def run(self, agents):
        snakes = self.snakes
        assert len(agents) == len(snakes)

        
        print("--------------------------- New Game ---------------------------\n")
        show = [[0] * 11 for _ in range(11)]
        for ID in range(len(self.state)):
            for i in range(11):
                for j in range(11):
                    if self.state[ID][i][j] > 0.5:
                        show[i][j] = ID + 1
                    elif self.state[ID][i][j] < 0.5:
                        show[i][j] = 9
        for row in show:
            print(row)
        print()
        
        
        # game procedures
        while len(snakes) > 1:
            
            # ask for moves
            for snake in snakes:
                new_head, old_head, tail = snake.move(agents[snake.id].make_move(self.states[snake.id]))
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
                    self.state[snake.id][tail[0]][tail[1]] = EMPTY
            
            # reduce health
            for snake in snakes:
                snake.health -= 1

            # check for food eaten
            remove_food = set()
            for snake in snakes:
                if snake.body[0] in self.food:
                    remove_food.add(snake.body[0])
                    snake.health = 100
                    snake.grow()
            # remove from list
            for food in remove_food:
                self.food.remove(food)
                # it is gonna be a head block so don't need to update the empty_posionts
                # unless two snakes of equal length meet on the food both die
                # in that case the dead snakes will be removed and don't need to worry about it here
                # just update the state
                # the snake's head will be recovered at the end of each turn
                for board in self.state:
                    board[food[0]][food[1]] = EMPTY
            
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
                    # not out of bound and not into a body
                    if head[0] >= 0 and head[0] < self.height and head[1] >= 0 and head[1] < self.width:
                        # head is in range
                        self.state[snake.id][head[0]][head[1]] = EMPTY
                        if head not in self.bodies:
                            self.empty_positions.add(head)
                else:
                    self.heads[head].remove(snake)
                    # there are more than one heads here, must be a head on or body collision and thus in range
                    self.state[snake.id][head[0]][head[1]] = EMPTY
                for i in range(1, len(snake.body)):
                    b = snake.body[i]
                    # it is possible that a snake has eaten on its first move and then die on its second move
                    # or it eats a food and die to head on collision
                    # in those two cases the snake will have a repeated tail
                    # remove it from bodies twice causes an error
                    try:
                        self.bodies.remove(b)
                        self.empty_positions.add(b)
                        self.state[snake.id][b[0]][b[1]] = EMPTY
                    except KeyError:
                        pass
                # clear the state board
                for food in self.food:
                    self.state[snake.id][food[0]][food[1]] = EMPTY
                snakes.remove(snake)

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
                    for snake in self.snakes:
                        self.state[snake.id][food[0]][food[1]] = EMPTY + (snake.health + HUNGER_a) * HUNGER_m
                except IndexError:
                    # Cannot choose from an empty set
                    pass
            
            # update the state
            for snake in self.snakes:
                board = self.state[snake.id]
                body = snake.body
                dist = len(snake.body)
                for b in snake.body:
                    board[b[0]][b[1]] = EMPTY + dist * SNAKE_m
                    dist -= 1

            
            show = [[0] * 11 for _ in range(11)]
            for ID in range(len(self.state)):
                for i in range(11):
                    for j in range(11):
                        if self.state[ID][i][j] > 0.5:
                            show[i][j] = ID + 1
                        elif self.state[ID][i][j] < 0.5:
                            show[i][j] = 9
            for row in show:
                print(row)
            print()
            

        # return the winner if there is one
        return tuple(snakes)[0].id if snakes else None
