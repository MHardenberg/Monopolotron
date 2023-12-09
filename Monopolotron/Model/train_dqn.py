from Monopolotron.Game.Game import Game
from Monopolotron.Model.DQNAgent import DQNAgent
from Monopolotron.Model.settings import max_turns
import Monopolotron.Model.utils as utils
from tqdm import tqdm


def train_dqn(dqn: DQNAgent, epochs: int, validation_interval: int = None,
              opponents: dict = {'cpu': 0, 'rnd_cpu': 3}, visualise=False):
    try:
        cpu_opponents = opponents['cpu']
    except KeyError:
        cpu_opponents = 0
    try:
        rnd_opponents = opponents['rnd_cpu']
    except KeyError:
        rnd_opponents = 0
    assert cpu_opponents + rnd_opponents > 0, \
        ValueError('Must supply at least 1 opponent.')

    net_losses, net_ties = 0, 0
    game_history = []
    win_outcome, tie_outcome, loss_outcome = 1, 0, -1

    for epoch in tqdm(range(epochs)):
        game_history += [win_outcome]
        game = Game(humans=0, cpu=cpu_opponents + 1,
                    rnd_cpu=rnd_opponents, dqn=dqn)
        for idx, _ in enumerate(game.players):
            game.players[idx].game = game

        done = False
        while len(game.players) > 1 and game.turns_played < max_turns\
                and not done:
            if visualise:
                game.visualise()

            for idx, p in enumerate(game.players):
                game.player_turn(idx)
                if game.players[idx].money <= 0:
                    if idx == 0:  # Implying that the net went bankrupt
                        dqn.memory.done()
                        net_losses += 1
                        game_history[-1] = loss_outcome
                        done = True

                    game.rem_bankrupt_player(idx)
            game.turns_played += 1
            dqn.replay()
            dqn.update_target()

            if game.turns_played == max_turns-1:
                net_ties += 1
                game_history[-1] = tie_outcome

        utils.save_game_stats(game, epoch, 'game_states.json')

    print(f'DQN win rate: {(epoch - net_losses - net_ties) / epoch}\n'
          f'Tie rate: {net_ties/epoch}',
          f'Results: {game_history}')
    return game_history





