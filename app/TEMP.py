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
That said, I am using a special trick, the value of a body block is equal to its distance to the tail,
so the head value will be the length of the snake. With this representation, one can recover the snakes
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

FOOD_factor = 1
BODY_factor = 1
HEAD_factor = 1
MYBODY_factor = 1
MY
EMPTY = 0
WALL = 1000

def interpret(data):
    """ Preprocess the data
    
    Args:
        data: the data defined by the
                Battlesnake Snake API (2020.01)
                https://docs.battlesnake.com/snake-api
    
    Return:
        grid: A grid that represents the game
    
    """

##    # gotta do the math to recenter the grid, fuck it's 2 in the morning. I will figure it out tomorrow
##    grid = [[EMPTY] * data['board']['height'] for row in range(data['board']['width'])]
##    
##    for food in data['board']['food']:
##        # I suppose a food is more wanted than an enmpty cell so let EMPTY be the base value
##        grid[food[0]][food[1]] -= data['you']['health'] * FOOD_factor
##    
##    for snake in data['board']['snakes']:
##        body = snake['body']
##        # get head
##        grid[body[0][0]][body[0][1]] = HEAD
##        # get the rest of the body
##        # Don't do the body[1:] slicing. It will copy the list
##        for i in range(1, len(body)):
##            grid[body[i][0]][body[i][1]] = BODY
##
##    body = data['you']['body']
##    # get head
##    grid[body[0][0]][body[0][1]] = MYHEAD
##    # get the rest of the body
##    for i in range(1, len(body)):
##        grid[body[i][0]][body[i][1]] = MYBODY
##    
##    return grid
