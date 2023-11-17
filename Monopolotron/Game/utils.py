import random
import json
import os


# load json to dict
def load_tile_set() -> dict:
    path = os.path.join(os.getcwd(), 'Monopolotron', 'Game', 'board.json')
    with open(path) as json_file:
        tile_set = json.load(json_file)

    tiles = {}
    for t in tile_set['tiles']:
        tiles[t['number']] = t
    return tiles


# dice and the like
def rolld6() -> int:
    return random.randint(1, 7)
