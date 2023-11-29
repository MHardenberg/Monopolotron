from Monopolotron.Game.Game import Game
from Monopolotron.Model.DQNAgent import DQNAgent
from Monopolotron.Model.settings import epochs, max_turns

if __name__ == "__main__":
    dqn = DQNAgent()
    lost = [0, 0]
    for epoch in range(epochs):
        print(f'Epoch {epoch} / {epochs}')
        game = Game(humans=0, cpu=1, rnd_cpu=1, dqn=dqn)
        for idx, _ in enumerate(game.players):
            game.players[idx].game = game

        while len(game.players) > 1 and game.turns_played < max_turns:
            #game.visualise()
            for idx, _ in enumerate(game.players):
                game.player_turn(idx)
                if game.players[idx].money <= 0:
                    dqn.memory.done()
                    lost[idx] += 1
                    break
            game.turns_played += 1
            dqn.replay()

    print(f'DQN win rate: {lost[1] / epochs}\n Random win rate: {lost[0] / epochs}')
