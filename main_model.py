from Monopolotron.Game.Game import Game
from Monopolotron.Model.DQNAgent import DQNAgent
from Monopolotron.Model.settings import max_turns, epochs
import time


train_model(visualise: bool=False, sleep_ms: float=0):
    dqn = DQNAgent()

    for epoch in range(1, epochs):
        game = Game(humans=0, cpu=2, rnd_cpu=0)
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
                    dqn.learn()



if __name__ == "__main__":
