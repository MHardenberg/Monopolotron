from Monopolotron.Game.Player import Player
from Monopolotron.Game.Game import Game
from Monopolotron.Game import settings
import time


if __name__ == "__main__":
    game = Game(players=2)

    game.players[0].jailed = True
    game.players[0].position = 10
    game.players[0].status = f'Status jailed for {0}'
    for _ in range(settings.board_length):
        print('-'*80 + '\n')

        for idx, _ in enumerate(game.players):
            game.players[idx].take_turn()
        print(game)
        time.sleep(1.5)

