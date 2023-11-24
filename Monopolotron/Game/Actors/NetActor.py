from Monopolotron.Game import Game
from Monopolotron.Game import Player
from Monopolotron.Game.Actors.RndActor import RndActor
from Monopolotron.Game import settings
from Monopolotron.Model.GameEncoder import GameEncoder
import numpy as np


class NetActor(RndActor):
    def __init__(self, player: Player, game: Game):
        super().__init__(player=player, game=game)
        self.encoder = GameEncoder()

    def decide_build(self, player: Player):
        """Handle buying buildings
        """
        print('Not implemented - acting as human')
        price = player.tile.cost_hotel if player.tile.buildings == 4 \
            else player.tile.cost_house
        if player.money < price:
            self.player.action += 'Property not bought.'
            print(f'Player {self.player.name} cannot afford to build on this tile.')
            return
        decision = self.__get_model_out(settings.build_prompt)
        if decision:
            player.tile.buildings += 1
            player.money -= price
            player.action += \
                f'Build! Currently {player.tile.buildings} on this property.'
            return
        self.player.action += 'Building not built.'

    def decide_buy(self,):
        """Handle buying properties.
        """
        print('Not implemented - acting as human')
        if self.player.money < self.player.tile.cost:
            self.player.action += 'Property not bought. '
            print(f'Player {self.player.name} cannot afford to build on this tile.')
            return
        if self._owned_another_player():
            return

        decision = self.__get_model_out(settings.buy_prompt)
        if decision:
            self.player.buy_property()
        else:
            self.player.action += 'Property not bought.'

    def __get_model_out(self, prompt: str) -> bool:
        print(self.__gather_inf())
        while True:
            ans = input(f'{prompt} [y/n]$ ')
            try:
                return {'y': True, 'n': False}[ans.lower()]
            except KeyError:
                print(f'Invalid input: {ans} - retry...')

    def __gather_inf(self) -> str:
        enc_game = self.encoder.encode_game(game=self.game, player=self.player)
        print(enc_game)
        return enc_game
