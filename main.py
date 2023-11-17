from Monopolotron.Game.Game import Game


if __name__ == "__main__":
    game = Game(players=2)

    game.players[0].jailed = True
    game.players[0].position = 10
    game.players[0].status = f'Status jailed for {0}'

    game.play(visualise=True)

