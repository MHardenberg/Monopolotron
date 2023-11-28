from Monopolotron.Game import Game
from Monopolotron.Game import Player
from Monopolotron.Game.Actors.RndActor import RndActor
from Monopolotron.Game import settings as game_settigns
from Monopolotron.Model import settings as model_settings
from Monopolotron.Model.GameEncoder import GameEncoder
from Monopolotron.Model.DQNAgent import DQNAgent
import torch


class NetActor(RndActor, model_state_dict: dict=False, dqn_model_instance: None):
    def __init__(self, player: Player, game: Game):
        super().__init__(player=player, game=game)
        self.encoder = GameEncoder()
        
        if dqn_model_instance:
            self.model = dqn_model_instance
        else:          
            self.model = DQNAgent()

        if model_state_dict:
            self.model.load_state_dict(model_state_dict)
        
        self.model.to(self.device)
        self.model.eval()

    def decide_build(self, player: Player):
        """Handle buying buildings
        """
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
        state = self.__gather_inf()
        action bool(self.model.act(state))

        # save to state action dict
        try:
            self.model.state_action_dict{self.player.player_number} += [(state, action),]
        except KeyError:
            self.model..state_action_dict{self.player.player_number} = [(state, action),]

        return action

    def __gather_inf(self) -> str:
        enc_game = self.encoder.encode_game(game=self.game, player=self.player)
        print(enc_game)
        return enc_game
