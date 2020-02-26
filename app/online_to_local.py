from game import Game
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

    this_food = {(food['y'], food['x']) for food in data['board']['food']}
    this_snakes = {Snake(snake['id'], snake['health'], [(b['y'], b['x']) for b in snake['body']]) for snake in data['board']['snakes']}
    you = Snake(data['you']['id'], data['you']['health'], [(b['y'], b['x']) for b in data['you']['body']])
    this_snakes.add(you)
    game = Game(data['board']['height'], data['board']['width'], food = this_food, snakes = this_snakes)
    
    return game, you
