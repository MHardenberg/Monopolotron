from Monopolotron.Game.Player import Player
#from Monopolotron.Game.Board import board
from Monopolotron.Game import settings


class Game:
    def __init__(self, players: int = 2) -> None:
        self.players: list = [Player() for _ in range(players)]

        # set starting money and pow
        for i in range(players):
            self.players[i].money = settings.player_funds
            self.players[i].name = settings.names[i]

#        self.board = board

    def __repr__(self,) -> str:
        
        out = settings.board_height * [settings.board_width * ['*']]
        for row_idx in range(len(out)):
            if row_idx == 0 or row_idx == settings.board_height - 1:
                out[row_idx] = ['O'] * settings.board_width
                continue

            out[row_idx][0] = out[row_idx][-1] = 'O'

        for p in self.players:
            pos = p.position
            rune = p.name[0]
            
            if pos < settings.board_width:
                out[-1][-(pos + 1)] = rune
                continue

            if pos < settings.board_width + settings.board_height -1:
                out[-(pos - settings.board_width + 2)][0] = rune
                continue

            if pos < 2*settings.board_width + settings.board_height -1:
                out[0][(pos - settings.board_width - settings.board_height +1)]\
                        = rune
                continue

            out[pos - 2*settings.board_width - settings.board_height][-1] = rune

        out[-1][-1] = '@'
        return '\n'.join(' '.join(row) for row in out)


