import json

from engine import (
    Player,
    Piece,
    Game,
    GameError
)

with open("dobutsu.json", "r") as rules_file:
    rules = json.load(rules_file)

p1 = Player("p1")
p2 = Player("p2")

game = Game(rules, p1, p2, first_player=0)

def print_board():
    for i in range(0, 12, 3):
        print(*game.board[i:i+3])

def move(p1, p2):
	try:
		game.move(p1, p2)
		game.next_turn()
	except GameError as e:
		print(e)

def place(h, p):
	try:
		game.place(h, p)
		game.next_turn()
	except GameError as e:
		print(e)

def hands():
	return game.hands


