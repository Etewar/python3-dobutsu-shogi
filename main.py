import json

from engine import (
    Player,
    Piece,
    Game
)

with open("dobutsu.json", "r") as rules_file:
    rules = json.load(rules_file)

p1 = Player("p1")
p2 = Player("p2")

game = Game(rules, p1, p2)

def print_board(game: Game):
    for i in range(0, 12, 3):
        print(*game.board[i:i+3])