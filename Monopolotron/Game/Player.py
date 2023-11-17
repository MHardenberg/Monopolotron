from Monopolotron.Game import utils
from Monopolotron.Game import settings


class Player:
    def __init__(self,) -> None:
        self.name: str = ''

        self.money: int = 0
        self.jailed: bool = False
        self.jailed_for_turns: int = 0
        self.properties: list = None

        self.position: int = 0
        self.status: str = ''

    def take_turn(self,):
        """ If not jailed, roll, move and evaluate game tile.. """
        if self.jailed:
            self.__handle_jail()
            return

        roll = 0, 0
        counter = 0
        res = 0

        while roll[0] == roll[1]:
            if counter > 2:
                # jail if rolling doubles more than twice
                self.__be_jailed()
                return

            roll = utils.rolld6(), utils.rolld6()
            res += sum(roll)
            counter += 1

            self.__update_pos(res)

        self.status = f'Status: On tile {self.position} rolled {counter} times'

    # Private methods
    def __be_jailed(self,):
        print(f"{self.name} jailed!")
        self.status = f'Status jailed for {self.jailed_for_turns}'
        self.position = settings.JAIL_POSITION
        self.jailed = True

    def __be_unjailed(self,):
        print(f"{self.name} unjailed!")
        self.status = f'Status: On tile {self.position} recently unjailed'
        self.jailed = False
        self.jailed_for_turns = 0

    def __handle_jail(self,):
        """  If the player rolls
        equal numbers on both dice, reroll unless jailed. Also, jail if
        player rolled a equal numbers for the third time.
        """

        roll1, roll2 = utils.rolld6(), utils.rolld6()
        if roll1 == roll2:  # set free on equal numbers
            self.__be_unjailed()
            return

        self.jailed_for_turns += 1
        if self.jailed_for_turns == 3:  # set free if jaild for 3 turns.
            self.__be_unjailed()
            return

        self.status = f'Status jailed for {self.jailed_for_turns}'

    def __update_pos(self, move: int, move_relative: bool = True):
        if not move_relative:
            self.position = move
            self.__eval_tile()
            return

        self.position += move

        # loop back
        self.position = self.position % settings.board_length
        self.__eval_tile()

    def __eval_tile(self):
        pass

    # magic
    def __repr__(self,) -> str:
        out = f'Player: {self.name}\n\t' + self.status
        return out
