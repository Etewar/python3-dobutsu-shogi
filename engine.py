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

        self.__turn = 0

        self.__active_player = first_player
    
    @property
    def active_player(self):
        return self.__active_player
    
    @property
    def turn(self):
        return self.__turn

    def move(self, pos1: int, pos2: int) -> bool:

        # if pos1, pos2 are in board
        if not (0 <= pos1 <= 11 and 0 <= pos2 <= 11):
            raise GameError("destination or initial location not in board")

        # if moving one tile
        if not (1 <= abs(pos1 - pos2) <= 4):
            raise GameError("must move one tile")
        
        # if there is no piece in pos1
        if self.board[pos1] is None:
            raise GameError("no piece in initial position")

        # if piece is owned by active player
        if not (self.board[pos1].owner is self.active_player):
            raise GameError("piece is not owned by active player")
        
        # if there is active player's piece in destination
        if self.board[pos2].owner is self.active_player:
            raise GameError("can not move onto own piece")
        
        # if piece can perform such move
        if not self.board[pos1].allowed_moves[
            (pos1 - pos2) * ((-1) ** self.board[pos1].owner) + 4]:
            raise GameError("piece can not move in such direction")
        
        # if there is opposing player's piece
        if self.board[pos2].owner is not self.active_player:
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

