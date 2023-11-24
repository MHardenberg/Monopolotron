from Monopolotron.Game.Game import Game


if __name__ == "__main__":
    game = Game(humans=0, cpu=0, rnd_cpu=2)
    print(game)
    for i, _ in enumerate(game.players):
        game.players[i].game = game

    game.play(visualise=True, speed_factor=100)
