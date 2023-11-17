from Monopolotron.Game import utils
from Monopolotron.Game import settings


class Player:
    def __init__(self,) -> None:
        self.name: str = ''

        self.money: int = 0
        self.jailed: bool = False
        self.properties: list = None

        self.position: int = 0

    def take_turn(self,):
        if self.jailed:
            # should ahndled jailed condition
            pass

        roll = 0, 0
        counter = 0
        res = 0

        while roll[0] == roll[1]:
            if counter > 2:
                self.jailed = True
                self.position = 10  # do better
                return

            roll = utils.rolld6(), utils.rolld6()
            res += sum(roll)
            counter += 1

            self.update_pos(res)
            self.eval_tile()

    def update_pos(self, move: int, move_relative: bool = True):
        if not move_relative:
            self.position = move
            # do eval
            return

        self.position += move

        # loop back
        self.position = self.position % settings.board_length
        print(f'Player {self.name} at ', self.position)
        self.eval_tile()

    def eval_tile(self):
        pass

    # magic
    def __repr__(self,) -> str:
        out = '\n'.join([f'Player: {self.name}',] +
                        ['\t' + field for field in dir(self) if not field.startswith('__')])
        return out
