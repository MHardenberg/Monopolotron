import torch

from Monopolotron.Game import Game
from Monopolotron.Game import Player
from Monopolotron.Model.DQNAgent import DQNAgent
from Monopolotron.Model.GameEncoder import GameEncoder
from Monopolotron.Model import DQNAgent
from Monopolotron.Model.Rewarder import Rewarder


class NetActor:
    def __init__(self, player: Player, game: Game, dqn=None):
        self.player: Player = player
        self.game: Game = game
        self.dqn=dqn
        self.encoder = GameEncoder()
        self.rewarder = Rewarder()

    def decide_build(self):
        """Handle buying building, always builds when enough money
        """
        price = self.player.tile.cost_hotel if self.player.tile.buildings == 4\
            else self.player.tile.cost_house
        if self.player.money >= price:
            self.player.tile.buildings += 1
            self.player.money -= price
            self.player.action += \
                    f'Build! Currently {self.player.tile.buildings} on this property.'



    def decide_buy(self,):
        """Handle buying properties.
        """
        encoded_state = self.encoder.encode_game(self.game, self.player).to(self.dqn.device)
        if self.player.money < self.player.tile.cost:
            self.player.action += f'Property not bought. Not enough money.'
            return
        else:
            buy = self.dqn.act(encoded_state)
            if buy.item() == 1:
                self.player.buy_property()
            else:
                self.player.action += f'Property not bought. DQN decided.'

        encoded_next_state = self.encoder.encode_game(self.game, self.player).to(self.dqn.device)
        reward = self._reward(encoded_next_state)
        self.player.action += f'Reward for this action: {reward}. '
        reward = torch.tensor(reward, device=self.dqn.device)
        done = torch.tensor(0, device=self.dqn.device)
        self.dqn.memory.update(encoded_state, buy, reward, encoded_next_state, done)

    def _reward(self, encoded_state) -> int:
        reward = self.rewarder.reward(self.player.player_number, encoded_state)
        return reward


    def _owned_another_player(self) -> bool:
        ''' For debugging, to assure players eventually
        buy whole street and can build.
        '''
        for idx, player in enumerate(self.game.players):
            if player != self.player and self.player.tile.street in \
                    player.properties.keys():
                return True
        return False




