from Monopolotron.Game.Player import Player
from Monopolotron.Game.Game import Game
from Monopolotron.Game import settings
import time


if __name__ == "__main__":
    game = Game(players=2)
    print(game)
    print(game.players[0])

    print('-'*80 + '\n')

    for _ in range(settings.board_length):
        print('-'*80 + '\n')

        for idx, _ in enumerate(game.players):
            game.players[idx].take_turn()
            print(game.players[idx].position)
        print(game)
        time.sleep(1.5)
