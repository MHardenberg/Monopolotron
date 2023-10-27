from Monopolotron.Game.Player import Player
#from Monopolotron.Game.Board import board
from Monopolotron.Game import settings
import numpy as np


class Game:
    def __init__(self, players: int = 2) -> None:
        self.players: list = [Player() for _ in range(players)]

        # set starting money and pow
        for i in range(players):
            self.players[i].money = settings.player_funds
            self.players[i].name = settings.names[i]

#        self.board = board

    def __repr__(self,) -> str:
        out = np.zeros((settings.board_width, settings.board_height + 2)).astype(str)
        out[:, :] = '*'
        out[:, 0] = 'O'; out[:, -1] = 'O'
        out[0, :] = 'O'; out[-1, :] = 'O'

        for p in self.players:
            pos = p.position
            rune = p.name[0]

            if pos < settings.board_width - 1:
                print('A')
                idx = -1, -(pos + 1)
                continue

            if pos < settings.board_width + settings.board_height - 1:
                print('B')
                idx = -(pos - settings.board_width), 0
                continue

            if pos < 2*settings.board_width + settings.board_height - 1:
                print('C')
                idx = 0, pos - settings.board_width - settings.board_height + 1
                continue

            idx = pos - 2*settings.board_width - settings.board_height, -1

        print(idx)
        out[idx[0]][idx[1]] = rune

        out[-1][-1] = '@'
        return '\n'.join(' '.join(row) for row in out)


