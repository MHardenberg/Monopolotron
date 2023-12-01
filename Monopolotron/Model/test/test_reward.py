from Monopolotron.Game.Game import Game
from Monopolotron.Model.Rewarder import Rewarder
from Monopolotron.Model.GameEncoder import GameEncoder
import Monopolotron.Model.settings as settings


def test_rewarder():
    game = Game(humans=2)
    player = game.players[0]
    encoder = GameEncoder()
    rewarder = Rewarder()

    # set initial value to zero, as we want to reward difference
    rewarder.player_hist[0] = 0.

    p_money = 123456.
    p_owns = [1, 3, 6, 8]
    p_houses = [5, 2, 0, 0]

    # calclate theexpeted reward
    expected_reward = settings.reward_multipliers['money'] * p_money\
        + settings.reward_multipliers['street'] * sum([
                game.board[x].cost for x in p_owns
                ])\
        + settings.reward_multipliers['house'] * sum([
                game.board[x].cost_house * p_houses[i]
                for i, x in enumerate(p_owns)
                ])

    # assign propeties and money.
    player.money = p_money
    for i, x in enumerate(p_owns):
        game.board[x].owner = player.name
        game.board[x].buildings = p_houses[i]

    state = encoder.encode_game(game, player)
    reward = rewarder.reward(player.player_number, state)

    print(state)
    assert reward == expected_reward, AssertionError(
            f'Reward not correct, is {reward} should be {expected_reward}.')
