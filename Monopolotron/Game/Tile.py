import json


class Tile:
    """ Should allow the players to see, whether it is owned, and what is does,
    cost and what not. """

    def __init__(self, d: dict) -> None:
        self.number: int
        self.name: str
        self.street: str
        self.type: str

        self.cost: int
        self.cost_house: int
        self.cost_hotel: int
        self.rent: list

        self.owner: str
        self.buildings: int

        for key, value in d.items():
            setattr(self, key, value)


