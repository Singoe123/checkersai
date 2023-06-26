from models import Piece


class Board:
    def __init__(self, player_pieces: list[Piece]=[], ai_pieces: list[Piece]=[], board = []):
        self.__player_pieces = player_pieces
        self.__ai_pieces = ai_pieces
        if board:
            for y in range(8):
                for x in range(8):
                    thisPiece = board[x][y]
                    if thisPiece in (1, 3):
                        self.__player_pieces.append(Piece(thisPiece > 2, y, x, False))
                    elif thisPiece in (2, 4):
                        self.__ai_pieces.append(Piece(thisPiece > 2, y, x, True))

    def set_player_pieces(self, pieces: list[Piece]):
        self.__player_pieces = pieces

    def set_ai_pieces(self, pieces: list[Piece]):
        self.__ai_pieces = pieces

    def get_player_pieces(self) -> list[Piece]:
        return self.__player_pieces

    def get_ai_pieces(self) -> list[Piece]:
        return self.__ai_pieces

    # For print(board) functionality, where board is an instance of Board

    def __str__(self):
        size = range(8)
        board = [[None] * 8 for _ in size]
        final_str = ""

        for piece in self.__player_pieces + self.__ai_pieces:
            board[piece.get_y_coordinate()][piece.get_x_coordinate()] = piece

        edge = "+ --- " * 8 + "+\n"

        for row in size:
            final_str += edge

            for column in size:
                if not board[row][column]:
                    final_str += "|     "
                else:
                    final_str += f"|  {str(board[row][column])}  "
            
            final_str += "|\n"
        
        final_str += edge
        return final_str
