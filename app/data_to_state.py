max_snakes = 8
EMPTY = 0.5
WALL = 1.0
MYHEAD = -1.0
# adders & mutipliers
# (value + value_a) * value_m
HUNGER_a = -100
HUNGER_m = 0.005
SNAKE_m = 0.01

def translate(data):
    """ Preprocess the data
    
    Args:
        data: the data defined by the
                Battlesnake Snake API (2020.01)
                https://docs.battlesnake.com/snake-api
    
    Return:
        state: the game state defined by game.py
    
    """

    height = data['board']['height']
    width = data['board']['width']

    state = [[[EMPTY] * width for row in range(height)] for layer in range(max_snakes)]

    health = data['you']['health']
    dist = len(data['you']['body'])
    for b in data['you']['body']:
        state[0][b['y']][b['x']] = EMPTY + dist * SNAKE_m
        dist -= 1
    for food in data['board']['food']:
        state[0][food['y']][food['x']] = EMPTY + (health + HUNGER_a) * HUNGER_m
    
    i = 1
    for snake in data['board']['snakes']:
        health = snake['health']
        dist = len(snake['body'])
        for b in snake['body']:
            try:
                state[i][b['y']][b['x']] = EMPTY + dist * SNAKE_m
            except IndexError:
                print(len(data['board']['snakes']), i, b)
                print("\n\n\n\n\n\n")
            dist -= 1
        for food in data['board']['food']:
            state[i][food['y']][food['x']] = EMPTY + (health + HUNGER_a) * HUNGER_m
        i += 1
    
    return state #, (data['you']['body'][0]['y'], data['you']['body'][0]['x'])
