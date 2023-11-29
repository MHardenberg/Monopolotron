import torch
import numpy as np


class GameEncoder:
    def __init__(self):
        self.street_enc = {
            'Brown': 1,
            'Light Blue': 2,
            'Pink': 3,
            'Orange': 4,
            'Red': 5,
            'Yellow': 6,
            'Green': 7,
            'Blue': 8,
            'rail': 9,
            'utilities': 10
            }

    def encode_game(self, game, player):
        board = game.board
        out = np.zeros(161 + 2*4)
        counter = 0

        for tile_key in board:
            tile = board[tile_key]
            to_add = [
                tile.number,
                self.street_enc[tile.street] if tile.street else 0,
                int(player.name == tile.owner) + 1 if tile.owner else 0,
                tile.buildings
            ]
            out[counter:counter+4] = to_add
            counter += 4
            #print(counter)

        for p in game.players:
            to_add = [
                p.position,
                p.money,
                    ]

            out[counter:counter+2] = to_add
            counter += 2

        out[-1] = game.turns_played
        out = torch.FloatTensor(out)
        return out
