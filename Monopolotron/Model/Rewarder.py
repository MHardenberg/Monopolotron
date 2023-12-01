import torch
import Monopolotron.Game.utils as utils
from Monopolotron.Model.GameEncoder import GameEncoder
import Monopolotron.Model.settings as settings


class Rewarder:
    def __init__(self):
        self.board: dict = utils.load_board()
        self.encoder = GameEncoder()
        self.player_hist: dict = {}

    def reward(self, player_idx: int, state: torch.Tensor) -> int:
        owned_streets = self.__find_owned_streets(state)
        money = int(state[161 + 2*player_idx])
        money_mult = settings.reward_multipliers['money']
        print(owned_streets)
        if not owned_streets.nelement():
            print("Returned")
            # comp to old val
            return money * money_mult

        owned_buildings =\
            self.__find_buildings_on_owned_streets(state, owned_streets).unsqueeze(dim=0)
        print(f'Streets shape {owned_streets.shape}')
        print(owned_buildings.shape)
        assets_values = money*money_mult +\
            sum([self.__find_tile_val(prop_num, houses_build) for
                prop_num, houses_build in
                zip(owned_streets, owned_buildings)])

        if player_idx not in self.player_hist:
            self.player_hist[player_idx] = [assets_values, ]
            return 0

        # compute reward as money plus assets
        # times their respective multipliers
        reward = assets_values - self.player_hist[player_idx][-1]
        self.player_hist[player_idx] += [assets_values, ]

        return reward

    def __find_owned_streets(self, state: torch.Tensor) -> torch.Tensor:
        """ Returns tensor of tile numbers oof owned streets """
        street_owned_code_pos = self.encoder.code_pos_dict['owned']
        return (state[street_owned_code_pos] == 1.).nonzero()

    def __find_buildings_on_owned_streets(self, state: torch.Tensor,
                                          owned_streets: torch.Tensor) -> torch.Tensor:
        """ Returns tensors of numbers of buildings on owned streets """
        if not owned_streets.nelement():
            print("not owned street")
            return torch.zeros_like(owned_streets)

        street_buildings_code_pos = self.encoder.code_pos_dict['buildings']
        print(f'Buildings {state[street_buildings_code_pos][owned_streets]}')
        return state[street_buildings_code_pos][owned_streets]

    def __find_tile_val(self, prop_num: int, houses_build: int) -> int:
        street_mult = settings.reward_multipliers['street']
        house_mult = settings.reward_multipliers['house']

        tile = self.board[int(prop_num)]
        return street_mult * tile.cost \
            + (min(4, houses_build) * tile.cost_house
                + int(houses_build == 5) * tile.cost_hotel) * house_mult
