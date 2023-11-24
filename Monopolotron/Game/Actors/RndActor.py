from Monopolotron.Game import Game
from Monopolotron.Game import Player
import random


class RndActor:
    def __init__(self, player: Player, game: Game):
        self.player: Player = player
        self.game: Game = game

    def decide_build(self, player: Player): 
        """Handle buying building, always builds when enough money
        """
        price = player.tile.cost_hotel if player.tile.buildings == 4 \
                else player.tile.cost_house
        if player.money >= price:
            player.tile.buildings += 1
            player.money -= price
            player.action += \
                    f'Build! Currently {player.tile.buildings} on this property.'

    def decide_buy(self,):
        """Handle buying properties.
        """
        buy = random.choice([True, False])
        if self.player.money >= self.player.tile.cost \
                and buy and not self._owned_another_player():
            self.player.buy_property()
        else:
            self.player.action += f'Property not bought. '

    def _owned_another_player(self) -> bool:
        ''' For debugging, to assure players eventually 
        buy whole street and can build.
        '''
        for idx, player in enumerate(self.game.players):
            if player != self.player and self.player.tile.street in \
                    self.player.properties.keys():
                return True
        return False




