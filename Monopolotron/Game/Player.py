from Monopolotron.Game import utils
from Monopolotron.Game import settings
from Monopolotron.Game import Game
from Monopolotron.Game.Actors.RndActor import RndActor
import random


class Player:
    def __init__(self, game: Game, actor=RndActor) -> None:
        """
        Initialize a new Player instance.

        Parameters:
        - game: An instance of the Game class.
        - actor: An actor instance responsible for decision-making.
        """
        self.name: str = ''

        self.money: int = 0
        self.jailed: bool = False
        self.jailed_for_turns: int = 0
        self.properties: dict = {}

        self.position: int = 0
        self.status: str = ''
        self.action: str = ''

        self.game: Game = game
        self.tile: dict = {}
        self.actor = actor(player=self, game=self.game)

    def take_turn(self, ):
        """ If not jailed, roll, move and evaluate game tile. """
        """ To add: add money when start passed"""
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

    def buy_property(self):
        cost = self.tile.cost
        street = self.tile.street
        self.money -= cost
        self.tile.owner = self.name
        if street not in self.properties:
            self.properties[street] = [self.tile]
        else:
            self.properties[street].append(self.tile)
        self.action += f'Bought property for {cost}. '

    def calculate_properties(self) -> int:
        try:
            return len(self.properties[self.tile.street])
        except KeyError:
            return 0

    def street_owned(self) -> bool:
        """
        Check if the player owns an entire street.

        Returns:
        True if the player owns the entire street, False otherwise.
        """
        street = self.tile.street
        return self.game.neighbourhoods[street] \
            == len(self.properties[street])

    # Private methods
    def __be_jailed(self, ):
        print(f"{self.name} jailed!")
        self.status = f'Status: jailed for {self.jailed_for_turns}'
        self.position = settings.JAIL_POSITION
        self.jailed = True

    def __be_unjailed(self, ):
        print(f"{self.name} unjailed!")
        self.status = f'Status: On tile {self.position} recently unjailed'
        self.jailed = False
        self.jailed_for_turns = 0

    def __handle_jail(self, ):
        """  If the player rolls
        equal numbers on both dice, reroll unless jailed. Also, jail if
        player rolled a equal numbers for the third time.
        """

        roll1, roll2 = utils.rolld6(), utils.rolld6()
        if roll1 == roll2:  # set free on equal numbers
            self.__be_unjailed()
            return

        self.jailed_for_turns += 1
        if self.jailed_for_turns == 3:  # set free if jailed for 3 turns.
            self.__be_unjailed()
            return

        self.status = f'Status jailed for {self.jailed_for_turns}'

    def __update_pos(self, move: int, move_relative: bool = True):
        """
        Update the player's position based on the dice roll.

        Parameters:
        - move: The number of spaces to move.
        - move_relative: Whether the movement is relative to the current position.
        """
        if not move_relative:
            self.position = move
            self.__eval_tile()
            return

        self.position += move

        # loop back
        if self.position >= settings.board_length:
            self.money += settings.money_over_go
            self.position = self.position % settings.board_length
        self.__eval_tile()

    def __eval_tile(self):
        self.tile = self.game.board[self.position]
        self.action += f'({self.tile.name}) '
        ops = {
            'road': self.__handle_property,
            'rail': self.__handle_rail,
            'utilities': self.__handle_utils,
            'go_jail': self.__be_jailed,
            'tax': self.__handle_tax,
            'chance': self.__handle_remaining,
            'jail': self.__handle_remaining,
            'chest': self.__handle_remaining,
            'parking': self.__handle_remaining,
            'start': self.__handle_remaining,
        }
        return ops.get(self.tile.type)()

    def __handle_property(self):
        owner = self.tile.owner
        if not owner:
            self.__decide_buy()
            return
        if owner != self.name:
            self.__pay_rent(self.tile.rent[self.tile.buildings])
            return
        if owner == self.name:
            if self.tile.buildings <= 4 and self.street_owned() \
                    and self.__street_buildings():

                self.__decide_build()

    def __handle_utils(self):
        owner = self.tile.owner
        if not owner:
            self.__decide_buy()
        elif owner != self.name:
            owned = self.calculate_properties()
            mult = sum((utils.rolld6(), utils.rolld6()))
            self.__pay_rent(self.tile.rent[owned] * mult)
        else:
            self.action += "Already owned. "

    def __handle_rail(self):
        owner = self.tile.owner
        if not owner:
            self.__decide_buy()
        elif owner != self.name:
            self.__pay_rent(self.tile.rent[self.calculate_properties()])
        else:
            self.action += "Already owned. "

    def __handle_tax(self):
        rent = self.tile.rent[0]
        self.money -= rent
        self.action += f'Payed {rent} tax. '

    def __handle_remaining(self):
        self.action += f'No action. '

    def __pay_rent(self, rent):
        """
        Pay rent to the owner of a property.

        Parameters:
        - rent: The amount of rent to pay.
        """

        idx = next(idx for idx, player in enumerate(self.game.players) \
                   if player.name == self.tile.owner)
        self.game.players[idx].money += rent
        self.money -= rent
        self.action += f'Payed {rent} rent. '

    def __print_properties(self) -> dict:
        properties = {}
        for key in self.properties.keys():
            for el in self.properties[key]:
                string = el.name + ':' + str(el.buildings)
                if key in properties.keys():
                    properties[key].append(string)
                else:
                    properties[key] = [string]
        return properties

    def __street_buildings(self) -> bool:
        street = self.tile.street
        for prop in self.properties[street]:
            if self.tile.buildings > prop.buildings:
                return False
        return True

    def __decide_build(self):
        self.actor.decide_build()

    def __decide_buy(self):
        self.actor.decide_buy()

# magic
    def __repr__(self, ) -> str:
        out = f'Player: {self.name}\n\t' + self.status + \
            f'\n\tAction: {self.action}' + f'\n\tBudget: {self.money}' + \
            f'\n\tProperties: {self.__print_properties()}'
        self.action = ''
        return out
