# board size
board_length: int = 40
board_width: int = board_length // 4 + 1
board_height: int = board_width


# starting settings
player_funds: int = 1500
money_over_go: int = 200
names = ['Harold', "Gavin A'Laugh", 'Willy Wonka', 'Steve']


# game constants
JAIL_POSITION = 10


# prompts
build_prompt = 'Do you want to build the next building on this tile?'
buy_prompt = 'Do you want to buy this tile?'
