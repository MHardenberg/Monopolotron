from Monopolotron.Game.Player import Player
from Monopolotron.Game import settings
from Monopolotron.Game.draw_board import draw_board_ascii
from Monopolotron.Game import utils
import os
import time


class Game:
    def __init__(self, players: int = 2) -> None:
        self.turns_played: int = 0
        self.board_drawer = draw_board_ascii()

        # populate players
        self.players: list = [Player() for _ in range(players)]
        self.bankrupt_players: list = []

        # set starting money and pow
        for i in range(players):
            self.players[i].money = settings.player_funds
            self.players[i].name = settings.names[i]

        # populate tiles
        self.tile_set = utils.load_tile_set()

    def play(self, visualise=False, max_turns=50):
        """ Start game loop until but one players are bankrupt or max turns 
        are reached.
        """
        while self.players and self.turns_played < max_turns:
            if visualise:
                # print board for debugging
                time.sleep(2)
                self.__visualise()

            for idx, p in enumerate(self.players):
                self.players[idx].take_turn()
                if p.money <= 0:
                    # remove bankrupt players
                    self.__rem_bankrupt_player(idx, p)

            self.turns_played += 1

    def __rem_bankrupt_player(self, bankrupt_players_idx, bankrupt_player):
        print(f'Player: {bankrupt_player.name} bankrupt!')
        self.bankrupt_players += [bankrupt_player,]
        # return player tiles to bank!
        print('WARINGIG NOT IMPLEMENTED!:' +
              'player tiles are not returned to bank')

        del self.players[bankrupt_players_idx]

    def __visualise(self,):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self)

    def __repr__(self,) -> str:
        out = f'Monopolotron on turn: {self.turns_played}\n'
        for p in self.players:
            out += p.__repr__() + '\n'
        return out + self.board_drawer.draw(self.players)
