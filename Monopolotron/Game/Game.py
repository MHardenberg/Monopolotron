from Monopolotron.Game.Player import Player
from Monopolotron.Game.Board import board
from Monopolotron.Game import settings


class Game:
    def __init__(self, players: int = 2) -> None:
        self.players: list = [Player() for _ in range(players)]

        # set starting money and pow
        for i in range(players):
            self.players[i].money = settings.players_funds
            self.players[i].name = settings.names[i]

        self.board = board

    def __repr__(self,) -> str:
        
        out = settings.board_height * [settings.board_width * '*']
        for row_idx in range(len(out)):
            if row_idx == 0 or row_idx == settings.board_height:
                out[row_idx] = ['_'] * settings.board_width
            out[row_idx[0]] = out[row_idx[-1]] = '_'

        return out

