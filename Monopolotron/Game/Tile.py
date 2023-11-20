from Monopolotron.Game.Player import Player
import json


class Tile:
    """ Should allow the players to see, whether it is owned, and what is does,
    cost and what not. """

    def __init__(self) -> None:
        self.number: int
        self.name: str
        self.street: str
        self.type: str

        self.can_be_bought: bool
        self.can_be_build: bool
        self.cost: int
        self.cost_house: int
        self.cost_hotel: int
        self.rent: list

        self.owner: Player
        self.buildings: list