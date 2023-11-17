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

    @classmethod
    def from_json(cls, json_data):
        tile = cls()
        tile.number = json_data["number"]
        tile.name = json_data["name"]
        tile.street = json_data["street"]
        tile.type = json_data["type"]
        tile.can_be_bought = json_data["can_be_bought"]
        tile.can_be_build = json_data["can_be_build"]
        tile.cost = json_data["cost"]
        tile.cost_house = json_data["cost_house"]
        tile.cost_hotel = json_data["cost_hotel"]
        tile.rent = json_data["rent"]
        tile.owner = json_data["owner"]
        tile.buildings = json_data["buildings"]
        return tile


def init_board() -> list:
    with open('board.json') as f:
        data = json.load(f)

    return [Tile.from_json(tile_data) for tile_data in data['tiles']]
