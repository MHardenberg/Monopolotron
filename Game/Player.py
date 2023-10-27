from Game import utils
from Game import settings


class Player:
    def __init__(self,) -> None:
        self.money: int
        self.jailed: bool
        self.properties: list = None

        self.position: int = 0

    def take_turn(self,):
        if self.jailed:
            pass

        roll = utils.rolld6(), utils.rolld6()
        res = sum(roll)
        counter = 1

        while roll[0] == roll[1]:
            if counter > 2:
                self.jailed = True
                self.position = 10 # do better
                return

            roll = utils.rolld6(), utils.rolld6()
            res += sum(roll)
            counter += 1

        
        self.position += res

    def update_pos(self, move: int, move_relative: bool=True):
        if not move_relative:
            self.position = move
            # do eval
            return

        self.position += move
        # loop back
        self.position -= self.position % settings.board_length

