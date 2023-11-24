from Monopolotron.Game.Game import Game
from Monopolotron.Model.DQNAgent import DQNAgent
from Monopolotron.Model.settings import max_turns, epochs
import time

if __name__ == "__main__":
    dqn = DQNAgent()
    for epoch in range(1, epochs):
        game = Game(humans=0, cpu=2, rnd_cpu=0)
        print(game)
        for idx, _ in enumerate(game.players):
            game.players[idx].game = game
            while len(game.players) > 1 and game.turns_played < max_turns:
                time.sleep(2/1000)
                game.visualise()
                game.play_turn()
                game.turns_played += 1
