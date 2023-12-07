import torch
import Monopolotron.Game.utils as utils
from Monopolotron.Model.GameEncoder import GameEncoder
import Monopolotron.Model.settings as model_settings
import Monopolotron.Game.settings as game_settings


class Rewarder:
    def __init__(self, game):
        self.board: dict = utils.load_board()
        self.encoder = GameEncoder()
        self.player_hist: dict = {}  # dict of past asset values
        self.game = game

    def reward(self, player_idx: int, state: torch.Tensor) -> int:
        if player_idx not in self.player_hist:
            self.player_hist[player_idx] = \
                    game_settings.player_funds\
                    * model_settings.reward_multipliers['money']

        owned_streets = self.__find_owned_streets(state)
        money = int(state[161 + 2*player_idx])

        # if we don't own any streets, we just hand the asset values as a tuple
        # to the __reward_from_asset_change method.
        if not owned_streets.nelement():
            assets = (money, 0, 0)
            return self.__reward_from_asset_change(player_idx, assets)

        owned_buildings =\
            self.__find_buildings_on_owned_streets(state, owned_streets)

        assets = money, \
            sum([
                    self.__find_tile_val(int(prop_num)) for
                    prop_num in owned_streets]), \
            sum([
                    self.__find_tile_building_val(int(prop_num),
                                                  int(buildings)) for
                    prop_num, buildings in zip(owned_streets, owned_buildings)
                    ])


        loss_multiplier = model_settings.reward_multipliers['loss']
        win_multiplier = model_settings.reward_multipliers['win']
        has_lost = money <= 0
        has_won = money > 0 and len(self.game.players) == 1

        reward = self.__reward_from_asset_change(player_idx, assets) - \
            loss_multiplier * int(has_lost) + \
            win_multiplier * int(has_won)

        return reward

    def __reward_from_asset_change(self, player_idx, current_assets) -> float:
        money, streets_value, buildings_value = current_assets

        money_mult = model_settings.reward_multipliers['money']
        street_mult = model_settings.reward_multipliers['street']
        house_mult = model_settings.reward_multipliers['house']

        net_worth = money_mult*money + street_mult*streets_value\
            + house_mult*buildings_value

        self.__update_player_hist(player_idx, net_worth)
        return net_worth
                # old metric: change_in_networth

    def __update_player_hist(self, player_idx, net_worth) -> None:
        self.player_hist[player_idx] = net_worth

    def __find_owned_streets(self, state: torch.Tensor) -> torch.Tensor:
        """ Returns tensor of tile numbers oof owned streets """
        street_owned_code_pos = self.encoder.code_pos_dict['owned']
        return (state[street_owned_code_pos] == 2.).nonzero()

    def __find_buildings_on_owned_streets(self, state: torch.Tensor,
                                          owned_streets: torch.Tensor) -> torch.Tensor:
        """ Returns tensors of numbers of buildings on owned streets """
        if not owned_streets.nelement():
            return torch.zeros_like(owned_streets)

        street_buildings_code_pos = self.encoder.code_pos_dict['buildings']
        return state[street_buildings_code_pos][owned_streets]

    def __find_tile_val(self, prop_num: int) -> int:
        tile = self.board[int(prop_num)]
        return tile.cost

    def __find_tile_building_val(self, prop_num: int, houses_build: int) -> int:
        tile = self.board[int(prop_num)]
        if tile.cost_house is None:
            return 0

        return (min(4, houses_build) * tile.cost_house
                + int(houses_build == 5) * tile.cost_hotel)
