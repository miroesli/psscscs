"""
Yang's Notes:

Deal with my shitty English.
I have put this into Google translator and the Chinese it gave me make sense so you are not allowed to complain.

Currently, I am assigning values to the cell to represent how preferable it is to avoid that cell.
The higher the value the more we should avoid it.
I know you probably want high values to be the one we want to go into but for the following reasons,
it is not very good to go with the opposite.

The direction of the body matters in some cases, but it makes no sense to say, for example,
verticle is 1 and horizontal is 2, since you should not argue that verticle is a lower value.
Additionally, I highly doubt the Artificial I is going to figure out the length thing by itself.
That said, I am using a special trick, the value of a body block is equal to its (scaled) distance to the tail,
so the head value will be the (scaled) length of the snake. With this representation, one can recover the snakes
nearly perfectly (there are degenerate cases but you can prove that they don't make a difference essentially).

I mean it makes sense. The tail is safer than the head, so it will have low values.
A long snake's head will be a major threat, so it has high values.

How to represent HP? Well, the more hungry we are the more we want food, the value of food indicates the HP.

It's also tricky to get a good representation of where our head is. We essentially only cares about the head,
since you cannot control the body and they work exactly as other snake's.
If you are a snake and I put you into the game, you will see everything around you and try to work out this maze.
So that's the idea, the view is centered at our head, meaning the center of the grid is always gonna be our head.
This is actually inspired by a YouTuber. Check it out! https://www.youtube.com/watch?v=-NJ9frfAWRo

We might want a representation for the HP of other snakes. I don't want to add any stuff beyond a grid
if not absolutely necessary.

I also have a plan to make the board more continuous, so the values change step by step instead of jumping.

I am going to ask Nishant cuz I think he once told us it is better to keep the values in the interval [0, 1].
"""

EMPTY = 0.5
WALL = 1.0
MYHEAD = -1.0
# adders & mutipliers
# (value + value_a) * value_m
HUNGER_a = -101
HUNGER_m = 0.005
SNAKE_m = 0.01

def preprocess(game, you, test_board = False, test_grid = False):
    """ Preprocess the data
    
    Args:
        game: a Game object defined by game.py
        you: a Snake object define by snake.py; represents this snake
    
    Return:
        grid: a grid that represents the game
    
    """
    
    # gotta do the math to recenter the grid
    width = (game.width + 1) * 2 - 1
    height = (game.height + 1) * 2 - 1
    grid = [[WALL] * width for row in range(height)]
    center = (width//2, height//2)
    # the original game board
    # it's easier to work on the original board then transfer it onto the grid
    board = [[EMPTY] * game.width for row in range(game.height)]
    
    # positions are (y, x) not (x, y)
    # because you read the grid row by row, i.e. (row number, column number)
    # otherwise the board is transposed
    for food in game.food:
        # I suppose a food is more wanted than an enmpty cell so let EMPTY be the base value
        board[food[0]][food[1]] += (you.health + HUNGER_a) * HUNGER_m
    
    my_length = len(you.body)
    for snake in game.snakes:
        body = snake.body
        # get head
        board[body[0][0]][body[0][1]] = EMPTY + (len(body) - (my_length - 1)) * SNAKE_m
        # get the rest of the body
        dist = len(body)
        # Don't do the body[1:] slicing. It will copy the list
        for i in range(1, len(body)):
            board[body[i][0]][body[i][1]] = EMPTY + dist * SNAKE_m
            dist -= 1
    
    # get my head
    head = you.body[0]
    board[head[0]][head[1]] = MYHEAD
    
    if test_board:
        print()
        for row in board:
            print(row)
        print()
    
    # from this point, all positions are measured relative to our head
    for y in range(game.height):
        for x in range(game.width):
            grid[y - head[0] + center[1]][x - head[1] + center[0]] = board[y][x]
    
    if test_grid:
        print()
        for row in grid:
            print(row)
        print()
    
    return grid
