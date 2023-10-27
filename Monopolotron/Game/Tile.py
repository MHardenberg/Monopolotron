from Monopolotron.Game.Player import Player


class Tile:
    """ Should allow the players to see, whether it is owned, and what is does, 
    cost and what not. """

    def __init__(self,) -> None:
        self.number: int
        self.can_be_bought: bool
        self.can_be_build: bool

        self.buildings: list
        self.cost: int
        self.rent: int

        self.street: int
        self.owner: Player
    

