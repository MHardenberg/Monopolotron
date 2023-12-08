import json


def save_game_stats(game, epoch, json_file):
    try:
        with open(json_file) as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    out = {
        'turns': game.turns_played,
        'board state': [],
            }

    for key in game.board:
        tile = game.board[key]
        street, owner, houses = tile.street, tile.owner, tile.buildings
        out['board state'] += [(street, owner, houses),]
        data[epoch] = out

    with open(json_file, "w") as f:
        json.dump(data, f)
