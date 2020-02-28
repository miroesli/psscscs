from snake import Snake

def translate(data):
    """ Translate the low speed data to high speed data
    
    Args:
        data: the data defined by the
                Battlesnake Snake API (2020.01)
                https://docs.battlesnake.com/snake-api
    
    Return:
        game: a Game object defined by game.py; represents the game
        you: a Snake object represents you
    
    """

    food = {(f['y'], f['x']) for f in data['board']['food']}
    snakes = {Snake(snake['id'], snake['health'], [(b['y'], b['x']) for b in snake['body']]) for snake in data['board']['snakes']}
    you = Snake(data['you']['id'], data['you']['health'], [(b['y'], b['x']) for b in data['you']['body']])
    snakes.add(you)
    game = Online_Game(data['board']['height'], data['board']['width'], food, snakes)
    
    return game, you

class Online_Game:

    def __init__(self, height, width, food, snakes):
        self.height = height
        self.width = width
        self.food = food
        self.snakes = snakes
