from Monopolotron.Game import Game
from Monopolotron.Game import Player
import random


class RndActor:
    def __init__(self, player: Player, game: Game, toddler=False):
        self.player: Player = player
        self.game: Game = game
        self.toddler = toddler

    def decide_build(self):
        """Handle buying building, always builds when enough money
        """
        price = self.player.tile.cost_hotel if self.player.tile.buildings == 4\
            else self.player.tile.cost_house
        if self.player.money >= price:
            self.player.build()

    def decide_buy(self,):
        """Handle buying properties.
        """
        buy = random.choice([True, False])
        if self.player.money >= self.player.tile.cost \
                and buy and not \
                (self._owned_another_player() and self.toddler):
            self.player.buy_property()
        else:
            self.player.action += f'Property not bought. '

    def _owned_another_player(self) -> bool:
        ''' For debugging, to assure players eventually
        buy whole street and can build.
        '''
        for idx, player in enumerate(self.game.players):
            if player != self.player and self.player.tile.street in \
                    player.properties.keys():
                return True
        return False



