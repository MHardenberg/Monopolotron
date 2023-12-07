import torch

from Monopolotron.Game import Game
from Monopolotron.Game import Player
from Monopolotron.Model.GameEncoder import GameEncoder
from Monopolotron.Model.Rewarder import Rewarder


class NetActor:
    def __init__(self, player: Player, game: Game, dqn=None):
        self.player: Player = player
        self.game: Game = game
        self.dqn = dqn
        self.encoder = GameEncoder()
        self.rewarder = Rewarder(self.game)

    def decide_build(self):
        """Handle buying building, always builds when enough money
        """
        price = self.player.tile.cost_hotel if self.player.tile.buildings == 4\
            else self.player.tile.cost_house

        if self.player.money < price:
            self.player.action += 'Not build. Not enough money.'
            return
        encoded_state = self.encoder.encode_game(self.game, self.player)\
            .to(self.dqn.device)
        buy = self.dqn.act(encoded_state)
        if buy.item() == 1:
            self.player.build()
        else:
            self.player.action += 'Not build. DQN decided.'

        encoded_next_state = self.encoder.encode_game(self.game, self.player)\
            .to(self.dqn.device)
        reward = self._reward(encoded_next_state)
        self.player.action += f'Reward for this action: {reward}. '
        reward = torch.tensor(reward, device=self.dqn.device)
        done = torch.tensor(0, device=self.dqn.device)
        self.dqn.memory.update(encoded_state, buy, reward,
                               encoded_next_state, done)

    def decide_buy(self,):
        """Handle buying properties.
        """
        if self.player.money < self.player.tile.cost:
            self.player.action += 'Property not bought. Not enough money.'
            return

        encoded_state = self.encoder.encode_game(self.game, self.player)\
            .to(self.dqn.device)
        buy = self.dqn.act(encoded_state)
        if buy.item() == 1:
            self.player.buy_property()
        else:
            self.player.action += 'Property not bought. DQN decided.'

        encoded_next_state = self.encoder.encode_game(self.game, self.player)\
            .to(self.dqn.device)
        reward = self._reward(encoded_next_state)
        self.player.action += f'Reward for this action: {reward}. '
        reward = torch.tensor(reward, device=self.dqn.device)
        done = torch.tensor(0, device=self.dqn.device)
        self.dqn.memory.update(encoded_state, buy, reward,
                               encoded_next_state, done)

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
