from Monopolotron.Game import Game
from Monopolotron.Game import Player
from Monopolotron.Game.Actors.RndActor import RndActor
from Monopolotron.Game import settings


class HumanActor(RndActor):
    def __init__(self, player: Player, game: Game):
        super().__init__(player=player, game=game)

    def decide_build(self, player: Player):
        """Handle buying buildings
        """
        price = player.tile.cost_hotel if player.tile.buildings == 4 \
            else player.tile.cost_house
        if player.money < price:
            self.player.action += 'Property not bought.'
            print(f'Player {self.player.name} cannot afford to build on this tile.')
            return
        decision = self.__get_input(settings.build_prompt)
        if decision:
            self.player.build()
            return
        self.player.action += 'Building not built.'

    def decide_buy(self,):
        """Handle buying properties.
        """
        print(self.player)
        if self.player.money < self.player.tile.cost:
            self.player.action += 'Property not bought. '
            print(f'Player {self.player.name} cannot afford to build on this tile.')
            return
        if self._owned_another_player():
            return

        decision = self.__get_input(settings.buy_prompt)
        if decision:
            self.player.buy_property()
        else:
            self.player.action += 'Property not bought.'

    def __get_input(self, prompt: str) -> bool:
        print(self.__gather_inf())
        while True:
            ans = input(f'{prompt} [y/n]$ ')
            try:
                return {'y': True, 'n': False}[ans.lower()]
            except KeyError:
                print(f'Invalid input: {ans} - retry...')

    def __gather_inf(self) -> str:
        tile_inf = [
                f'Tile {self.player.tile.number}: {self.player.tile.name}',
                f'Street: {self.player.tile.street}',
                f'{self.player.tile.type}',
                f'Cost: {self.player.tile.cost}',
                ]
        player_inf = [
                f'Funds: {self.player.money}',
                f'Owned prop. on that street: {self.player.calculate_properties()}',
                ]

        return '\n'.join(tile_inf + player_inf)
