from Monopolotron.Game.Game import Game
from Monopolotron.Model.DQNAgent import DQNAgent
from Monopolotron.Model.settings import epochs, max_turns
from tqdm import tqdm

if __name__ == "__main__":
    dqn = DQNAgent()
    results = [0, 0, 0, 0, 0]
    for epoch in tqdm(range(epochs)):
        game = Game(humans=0, cpu=1, rnd_cpu=3, dqn=dqn)
        for idx, _ in enumerate(game.players):
            game.players[idx].game = game

        while len(game.players) > 1 and game.turns_played < max_turns:
            #game.visualise()
            for idx, _ in enumerate(game.players):
                game.player_turn(idx)
                if game.players[idx].money <= 0:
                    dqn.memory.done()
                    results[idx] += 1
                    # this doesn't work 
                    game.rem_bankrupt_player(idx)
                    break
            game.turns_played += 1
            dqn.replay()
            if game.turns_played == max_turns-1:
                results[2] += 1

    print(f'DQN win rate: {sum([results[x] for x in range(1, game.original_player_num)]) / (epochs*(game.original_player_num-1))}\n'
          f'Random win rate: {results[0] / epochs}\n'
          f'Tie rate: {results[-1]/epochs}')
    print(results)
