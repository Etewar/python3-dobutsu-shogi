class GameError(Exception):
    pass

class Player:
    
    def __init__(self, name: str):
        self.name = name
    
    def __str__(self):
        return "<Player: {0}>".format(self.name)
    
    def __repr__(self):
        return "<Player: {0}>".format(self.name)

class Piece:


    def __init__(self, owner: int, name: str, allowed_moves: list, 
                 upgraded_allowed_moves: list = None, upgraded: bool = False):

        self.__name = name
        self.__owner = owner
        self.__allowed_moves = allowed_moves
        self.__upgraded = upgraded
        
        if upgraded_allowed_moves == None:
            self.__upgraded_allowed_moves = allowed_moves
        else:
            self.__upgraded_allowed_moves = upgraded_allowed_moves
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, val):
        if isinstance(val, str):
            self.__name = val
        else:
            raise TypeError("name must be member of str class")
    
    @property
    def owner(self) -> Player:
        return self.__owner
    
    @owner.setter
    def owner(self, val: int):
        self.__owner = val
    
    @property
    def allowed_moves(self) -> list:
        if self.upgraded:
            return self.__upgraded_allowed_moves
        else:
            return self.__allowed_moves
    
    @property
    def upgraded(self) -> bool:
        return self.__upgraded
    
    def upgrade(self):
        self.__upgraded = True

    def is_move_allowed(self, pos1, pos2) -> bool:
        return self.allowed_moves[(pos1 - pos2) * ((-1) ** self.owner) + 4]
    

    def __str__(self):
        return "<Piece: {0}, owner: {1}>".format(self.name, self.owner)
    
    def __repr__(self):
        return "<Piece: {0}, owner: {1}>".format(self.name, self.owner)



class Game:

    def __init__(self, mode: dict, player1: Player, player2: Player, 
                 first_player: bool = 0):
        
        #self.rules = mode
        self.players = (player1, player2)

        self.hands = ([], [])
        self.board = [None for _ in range(mode["RULES"]["board_size"])]
        
        for p_type, pos in mode["RULES"]["starting_layout"]["player1"]:
            self.board[pos] = Piece(0, **mode["PIECES"][p_type])
            
        for p_type, pos in mode["RULES"]["starting_layout"]["player2"]:
            self.board[pos] = Piece(1, **mode["PIECES"][p_type])
                    
        self.__first_player = first_player

        self.__turn = 1

        self.__active_player = first_player
    
    @property
    def active_player(self):
        return self.__active_player
    
    @property
    def turn(self):
        return self.__turn

    def avialable_moves(self, pos: int) -> list:

        adjacent_squares = [
            [1, 3, 4],
            [0, 2, 3, 4, 5],
            [1, 4, 5],
            [0, 1, 4, 6, 7],
            [0, 1, 2, 3, 5, 6, 7, 8],
            [1, 2, 4, 7, 8],
            [3, 4, 7, 9, 10],
            [3, 4, 5, 6, 8, 9, 10, 11],
            [4, 5, 7, 10, 11],
            [6, 7, 10],
            [6, 7, 8, 9, 11],
            [7, 8, 10]
        ]
        avialable = set()

        if self.board[pos] is not None:
            for potential in adjacent_squares[pos]:
                if self.board[potential]:
                    if self.board[potential].owner is not self.board[pos].owner:
                        avialable.add(potential)
                    else:
                        continue
                if (self.board[pos].is_move_allowed(pos, potential)):
                    avialable.add(potential)

        return list(avialable)


    def move(self, pos1: int, pos2: int) -> bool:

        # if can perform move
        if pos2 not in self.avialable_moves(pos1):
            raise GameError("can not perform such move")
        
        # if moving not own piece
        if self.board[pos1].owner is not self.active_player:
            raise GameError("can not move opposing player's piece")

        # if there is opposing player's piece
        if self.board[pos2] is not None:
            self.board[pos2].owner = self.active_player
            self.board[pos2].__upgraded = False
            self.hands[self.active_player].append(self.board[pos2])
        
        self.board[pos2], self.board[pos1] = self.board[pos1], None
    
    def place(self, hand_pos: int, board_pos: int):

        # if board_pos are in board
        if not (0 <= board_pos <= 11):
            raise GameError("destination or initial location not in board")
        
        # if there is a piece in board_pos
        if self.board[board_pos] is not None:
            raise GameError("piece in destination")
        
        try:
            self.board[board_pos] = self.hands[self.active_player][hand_pos]
        except IndexError:
            raise GameError("invalid hand piece position")
        
        del self.hands[self.active_player][hand_pos]

    def next_turn(self):
        self.__turn += 1
        self.__active_player = int(not self.__active_player)

