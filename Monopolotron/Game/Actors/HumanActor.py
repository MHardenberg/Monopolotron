from Monopolotron.Game import Game
from Monopolotron.Game import Player
from Monopolotron.Game.Actors.RndActor import RndActor
import random


class HumanActor(RndActor):
    def __init__(self, player: Player, game: Game):
        super().__init__(player=player, game=game)

    def decide_build(self, player: Player): 
        """Handle buying buildings
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
                and buy and not self.__owned_another_player():
            self.player.buy_property()
        else:
            self.player.action += f'Property not bought. '


    def __get_input(self, prompt: str) -> bool:
        ans = input(f'{msg} $ []')
