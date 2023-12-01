from Monopolotron.Game.Game import Game
from Monopolotron.Model.DQNAgent import DQNAgent
from Monopolotron.Model.settings import max_turns, epochs
import time


train_model(visualise: bool=False, sleep_ms: float=0):
    dqn = DQNAgent()

    for epoch in range(1, epochs):
        game = Game(humans=0, cpu=2, rnd_cpu=0, dqn_model_instance=dqn)
        for idx, _ in enumerate(game.players):

            game.players[idx].game = game
            while not game.finished:
                if sleep_ms:
                    time.sleep(0.001 * sleep_ms)
                if visualise:
                    game.visualise()

                game.play_turn()
                game.turns_played += 1

                done = game.finished
                for idx, _ in enumerate(game.players):
                    state_action_list = state_action_dict[idx]
                    while state_action_list:
                        state, action = state_action_list.pop(0)
                        final_move = (len(state_action_list) == 0) and done
                        dqn.replay(idx, state, action, final_move)
                        dqn.clear_state_action_dict()



if __name__ == "__main__":
