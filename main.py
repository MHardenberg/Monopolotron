from Monopolotron.Game.Player import Player
from Monopolotron.Game.Game import Game
from Monopolotron.Game import settings
import time


if __name__ == "__main__":
    game = Game(players=1)
    print(game)
    print(game.players[0])

    print('-'*80 + '\n')

    for _ in range(settings.board_length):
        print('-'*80 + '\n')
        print(game)

        game.players[0].position += 1
        time.sleep(.5)

