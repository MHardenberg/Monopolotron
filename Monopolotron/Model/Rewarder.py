import torch
import Monopolotron.Game.utils as utils
from Monopolotron.Model.GameEncoder import GameEncoder
import Monopolotron.Model.settings as model_settings
import Monopolotron.Game.settings as game_settings
import csv


class Rewarder:
    def __init__(self):
        self.board: dict = utils.load_board()
        self.encoder = GameEncoder()
        self.player_hist: dict = {}  # dict of past asset values
        self.total_reward = {}

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

        outcome_reward = 0
        if self.__check_loss(player_idx, state):
            outcome_reward = model_settings.reward_multipliers['defeat']
        elif self.__check_win(player_idx, state):
            outcome_reward = model_settings.reward_multipliers['victory']

        reward = outcome_reward +\
                self.__reward_from_asset_change(player_idx, assets)
        try:
            self.total_reward[player_idx] += reward
        except KeyError:
            self.total_reward[player_idx] = reward

        return reward

    def save_total(self):
        with open('stats/reward.csv', 'a') as f:
            write = csv.writer(f)
            out = [self.total_reward[key] for key in self.total_reward]
            write.writerow(out)

    def __reward_from_asset_change(self, player_idx, current_assets) -> float:
        money, streets_value, buildings_value = current_assets

        money_mult = model_settings.reward_multipliers['money']
        street_mult = model_settings.reward_multipliers['street']
        house_mult = model_settings.reward_multipliers['house']

        net_worth = money_mult*money + street_mult*streets_value\
            + house_mult*buildings_value

        change_in_networth = net_worth - self.player_hist[player_idx]
        self.__update_player_hist(player_idx, net_worth)

        return change_in_networth

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

    def __check_win(self, player_idx: int, state: torch.Tensor):
        money_pos = self.encoder.code_pos_dict['money'].copy()
        own_money_pos = money_pos.pop(player_idx)
        return all(state[p] <= 0 for p in money_pos)

    def __check_loss(self, player_idx: int, state: torch.Tensor):
        money_pos = self.encoder.code_pos_dict['money'][player_idx]
        return (state[money_pos] <= 0)
