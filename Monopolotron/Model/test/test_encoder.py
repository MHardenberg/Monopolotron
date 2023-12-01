from Monopolotron.Model.GameEncoder import GameEncoder
from Monopolotron.Game.Game import Game 
from Monopolotron.Game.Player import Player


def test_game_encoder():
    enc = GameEncoder()
    game = Game(humans = 2)
    player = game.players[0]
    p_pos = 20
    p_money = 12345

    player.position = p_pos
    player.money = p_money
    
    encoding = enc.encode_game(game=game, player=player)

    assert encoding[160] == p_pos,\
        AssertionError("Posisiton noty encoded correctly")
    assert encoding[161] == p_money,\
        AssertionError("Money noty encoded correctly")


