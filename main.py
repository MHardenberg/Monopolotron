from Monopolotron.Game.Game import Game


if __name__ == "__main__":
    game = Game(humans=1, cpu=1, rnd_cpu=1)

    game.players[0].jailed = True
    game.players[0].position = 10
    game.players[0].status = f'Status jailed for {0}'
    game.players[0].game = game
    game.players[1].game = game

    game.play(visualise=True, speed_factor=1)
