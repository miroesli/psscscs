import random

from snake import Snake

class Game:
    
    def __init__(self, height, width, snake_cnt):
        assert snake_cnt <= 8
        # empty_positions is used to generate food randomly
        self.empty_positions = {(y, x) for y in range(height) for x in range(width)}
        # standard board positions (in order) for 7x7, 11x11, and 19x19
        # battlesnake uses random positions for any non-standard board size
        # https://github.com/BattlesnakeOfficial/engine/blob/master/rules/create.go
        positions = [
            (1, 1), (height - 2, width - 2), (height - 2, 1), (1, width - 2),
            (1, width//2), (height//2, width - 2), (height - 2, width//2), (height//2, 1)
        ]
        # I changed the data structure to speed up the game
        self.height = height
        self.width = width
        self.snakes = {Snake(ID, 100, [positions[ID]] * 3) for ID in range(snake_cnt)}
        for snake in self.snakes:
            self.empty_positions.remove(snake.body[0])
        self.food = set(random.sample(self.empty_positions, snake_cnt))
        for food in self.food:
            self.empty_positions.remove(food)
        
        # two board sets are used to reduce run time
        self.heads = {snake.body[0]: {snake} for snake in self.snakes}
        self.bodies = {snake.body[i] for snake in self.snakes for i in range(1, len(snake.body))}

    # game rules
    # https://github.com/BattlesnakeOfficial/rules/blob/master/standard.go
    # this link below is what they use for the engine, and for fuck sake they have defferent algorithms, resulting in different rules
    # https://github.com/BattlesnakeOfficial/engine/blob/master/rules/tick.go
    # I am using the online version (first one)
    def run(self, agents):
        snakes = self.snakes
        assert len(agents) = len(snakes)
        
        # game procedures
        while len(snakes) > 1:
            
            # ask for moves
            for snake in snakes:
                new_head, old_head, tail = snake.move(agents[snake.id].make_move(self, snake))
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
                        if len(snake.body) <= len(s.body):
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
                    self.empty_positions.add(head)
                else:
                    self.heads[head].remove(snake)
                for i in range(1, len(snake.body)):
                    self.bodies.remove(snake.body[i])
                    self.empty_positions.add(snake.body[i])
                snakes.remove(snake)
            
            # check for food eaten
            # the original battlesnake uses a for loop on an array since they don't care about speed
            remove_food = set()
            for snake in snakes:
                if snake.body[0] in self.food:
                    remove_food.add(snake.body[0])
                    snake.health = 100
                    snake.grow()
            # remove eaten food
            for food in remove_food:
                self.food.remove(food)

            # spawn food
            if len(self.food) == 0:
                chance = 1.0
            else:
                chance = 0.15
            if random.random() <= chance:
                try:
                    food = random.choice(tuple(self.empty_positions))
                    self.food.add(food)
                    self.empty_positions.remove(food)
                except IndexError:
                    # Cannot choose from an empty set
                    pass

        # return the winner if there is one
        return tuple(snakes)[0].id if snakes else None
