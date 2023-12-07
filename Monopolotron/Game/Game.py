from Monopolotron.Game.Player import Player
from Monopolotron.Game.Actors.HumanActor import HumanActor
from Monopolotron.Game.Actors.RndActor import RndActor
from Monopolotron.Game.Actors.NetActor import NetActor
from Monopolotron.Game import settings
from Monopolotron.Game.draw_board import draw_board_ascii
from Monopolotron.Game import utils
import os
import time


class Game:
    def __init__(self, humans: int = 0, cpu=0, rnd_cpu: int = 2,
                 dqn = None) -> None:
        self.humans, self.cpu, self.rnd_cpu, self.dqn = humans, cpu, rnd_cpu,\
                dqn

        self.turns_played: int = 0
        self.board_drawer = draw_board_ascii()

        # populate players
        players = humans + cpu + rnd_cpu
        assigned_players = 0
        self.original_player_num: int = players
        self.players: list = [Player(game=self,
                                     player_number=assigned_players + i,
                                     actor=HumanActor) for i in range(humans)]
        assigned_players += humans
        self.players += [Player(game=self,
                                player_number=assigned_players + i,
                                actor=NetActor, dqn=dqn) for i in range(cpu)]

        self.players += [Player(game=self, player_number=assigned_players +i,
                                actor=RndActor) for i in range(rnd_cpu)]

        self.bankrupt_players: list = []

        # set starting money and pow
        for i in range(players):
            self.players[i].money = settings.player_funds
            self.players[i].name = settings.names[i]

        # populate tiles
        # self.tile_dict: dict = utils.load_tile_set()
        self.board: dict = utils.load_board()
        self.neighbourhoods: dict = utils.sum_neighbourhoods(self.board)

    def play(self, visualise=False, max_turns=100, speed_factor=1):
        """ Start game loop until but one players are bankrupt or max turns
        are reached.
        """
        while len(self.players) > 1 and self.turns_played < max_turns:
            if visualise:
                # print board for debugging
                time.sleep(2/speed_factor)
                self.__visualise()
                self.__play_turn()
                self.turns_played += 1

    def player_turn(self, idx: int):
        self.players[idx].take_turn()

    def rem_bankrupt_player(self, bankrupt_players_idx):
        del self.players[bankrupt_players_idx]

    def reset(self):
        for p in self.players:
            del p
        self.__init__(self.humans, self.cpu, self.rnd_cpu, self.dqn)

    def __play_turn(self,):
        for idx, p in enumerate(self.players):
            self.players[idx].take_turn()
            if p.money <= 0:
                # remove bankrupt players
                self.__rem_bankrupt_player(idx, p)

    def __rem_bankrupt_player(self, bankrupt_players_idx, bankrupt_player):
        print(f'Player: {bankrupt_player.name} bankrupt!')
        self.bankrupt_players += [bankrupt_player,]
        # return player tiles to bank!
        print('WARNING NOT IMPLEMENTED!:' +
              'player tiles are not returned to bank')

        del self.players[bankrupt_players_idx]

    def visualise(self,):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self)

    def __repr__(self,) -> str:
        out = f'\nMonopolotron on turn: {self.turns_played}\n'
        for p in self.players:
            out += p.__repr__() + '\n'
        return out + self.board_drawer.draw(self.players)
