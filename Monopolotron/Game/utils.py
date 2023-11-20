import random
import json
import os
from Monopolotron.Game.Tile import Tile


# load json to dict
def load_tile_set() -> dict:
    path = os.path.join(os.getcwd(), 'Monopolotron', 'Game', 'board.json')
    with open(path) as json_file:
        tile_set = json.load(json_file)

    tiles = {}
    for t in tile_set['tiles']:
        tiles[t['number']] = t
    return tiles


def load_board() -> dict:
    path = os.path.join(os.getcwd(), 'Monopolotron', 'Game', 'board.json')
    with open(path) as json_file:
        tile_set = json.load(json_file)
    board = {}
    for t in tile_set['tiles']:
        board[t['number']] = Tile(t)
    return board


def sum_neighbourhoods(tiles: dict) -> dict:
    neighbourhoods = {}
    for tile in tiles.values():
        street = tile.street
        if street in neighbourhoods:
            neighbourhoods[street] += 1
        else:
            neighbourhoods[street] = 1
    return neighbourhoods


# dice and the like
def rolld6() -> int:
    return random.randint(1, 7)
