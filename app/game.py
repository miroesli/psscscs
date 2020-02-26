import random

from snake import Snake
import agent

class Game:
    
    def __init__(self, height = 11, width = 11, snake_cnt = 8, food = None, snakes = None):
        # translated game
        if snakes:
            self.height = height
            self.width = width
            self.food = food
            self.snakes = snakes
        # new game
        else:
            assert snake_cnt <= 8
            # board_positions is used to generate food randomly
            self.board_positions = [(y, x) for y in range(height) for x in range(width)]
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
            self.food = set(random.sample(self.board_positions, snake_cnt))
            self.snakes = {Snake(ID, 100, [positions[ID]] * 3) for ID in range(snake_cnt)}
        
        # two board sets are used to reduce run time
        self.heads = {snake.body[0]: {snake} for snake in self.snakes}
        self.bodies = {snake.body[i] for snake in self.snakes for i in range(1, len(snake.body))}
    
    def run(self):
        # game procedures
        # https://github.com/BattlesnakeOfficial/engine/blob/master/rules/tick.go
        while len(snakes) > 1:
            snakes = self.snakes
            # ask for moves
            for snake in snakes:
                new_head, old_head, tail = snake.move(Agent.make_move(self, snake))
                # update board sets
                try:
                    self.heads[new_head].add(snake)
                except KeyError:
                    self.heads[new_head] = {snake}
                if len(self.heads[old_head]) == 1:
                    del self.heads[old_head]
                else:
                    self.heads[old_head].remove(snake)
                self.bodies.add(old_head)
                self.bodies.remove(tail)

            # check for food eaten
            # the original battlesnake uses a for loop on an array since they don't care about speed
            remove_food = {}
            for snake in self.snakes:
                if snake.body[0] in self.food:
                    remove_food.add(snake.body[0])
                    snake.health = 100
                    snake.grow()
                # not eating; reduce health
                else:
                    snake.health -= 1

            # remove eaten food
            for food in remove_food:
                self.food.remove(food)
            
            # remove dead snakes
            # I have checked the code of the battlesnake game
            # there algorithm for checking collisions is shit
            # they run a nested for loop for every snake
            # this whole check through runs in O(n) time
            # the rules are here
            # https://github.com/BattlesnakeOfficial/engine/blob/master/rules/death.go
            kills = {}
            for snake in self.snakes:
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
            
            # remove dead snakes
            for snake in kills:
                # update board sets
                head = snake.body[0]
                if len(self.heads[head]) == 1:
                    del self.heads[head]
                else:
                    self.heads[head].remove(snake)
                for i in range(1, len(snake.body)):
                    self.bodies.remove(snake.body[i])
                snakes.remove(snake)
        
        print("Game ended, snake", snakes[0].id, "won!")
