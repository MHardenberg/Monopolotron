from Monopolotron.Game import Game
from Monopolotron.Game import Player
from Monopolotron.Game.Actors.RndActor import RndActor
from Monopolotron.Game import settings
import numpy as np


class NetActor(RndActor):
    def __init__(self, player: Player, game: Game):
        super().__init__(player=player, game=game)
        self.type_enc = {
            'road': 1,
            'chest': 2,
            'tax': 3,
            'rail': 4,
            'chance': 5,
            'jail': 6,
            'utilities': 7,
            'parking': 8,
            'go-jail': 9,
                }

        self.colour_enc = {
            'Brown': 1,
            'Light Blue': 2,
            'Pink': 3,
            'Orange': 4,
            'Red': 5,
            'Yellow': 6,
            'Green': 7,
            'Blue': 8
            }

    def decide_build(self, player: Player):
        """Handle buying buildings
        """
        print('Not implemented - actiing as human')
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
        print('Not implemented - actiing as human')
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
        tile_inf = [
                self.player.tile.number,
                self.__encode_colour(self.player.tile.street),
                self.__encode_type(self.player.tile.type),
                self.player.tile.cost,
                ]
        player_inf = [
                self.player.money,
                self.player.calculate_properties(),
                ]

        out = np.array(tile_inf + player_inf)
        print('Model in:', out)
        return out

    def __encode_colour(self, colour) -> int:
        if not colour:
            return 0
        return self.colour_enc[colour]

    def __encode_type(self, type) -> int:
        if not type:
            return 0
        return self.type_enc[type]
