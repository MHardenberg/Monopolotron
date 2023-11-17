from Monopolotron.Game.Player import Player
#from Monopolotron.Game.Board import board
from Monopolotron.Game import settings
from Monopolotron.Game.draw_board import draw_board_ascii

class Game:
    def __init__(self, players: int = 2) -> None:
        self.players: list = [Player() for _ in range(players)]

        # set starting money and pow
        for i in range(players):
            self.players[i].money = settings.player_funds
            self.players[i].name = settings.names[i]

        self.board_drawer = draw_board_ascii()
        

    def __repr__(self,) -> str:
        return self.board_drawer.draw(self.players)
        
