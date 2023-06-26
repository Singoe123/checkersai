from models import Board
from models import Piece


class Game:
    def __init__(self, base: Board) -> None:
        self.whites = 0
        self.blacks = 0
        self.wQueens = 0
        self.bQueens = 0
        self.turn = False
        self.board = [[0] * 8 for _ in range(8)]
        self.winner = -1
        self.emp = 0
        self.historial = []

        for piece in base.get_player_pieces():
            if piece.get_is_queen():
                thisPiece = 3
                self.wQueens += 1
            else:
                thisPiece = 1
            self.board[piece.get_x_coordinate()][piece.get_y_coordinate()] = thisPiece
            self.whites += 1

        for piece in base.get_ai_pieces():
            if piece.get_is_queen():
                thisPiece = 4
                self.bQueens += 1
            else:
                thisPiece = 2
            self.board[piece.get_x_coordinate()][piece.get_y_coordinate()] = thisPiece
            self.blacks += 1

        self.moves = self.posibleMoves()
        self.takes = self.posibleTakes()

    def checkWinner(self):
        if self.moves == [] and self.takes == []:
            if self.emp >= 40:
                return 0
            if self.blacks == 0:
                return 1
            if self.whites == 0:
                return 2
            return 0
        return -1

    def getEstado(self):
        r = self.checkWinner()
        if r == 1:
            return float('inf')
        if r == 2:
            return float('-inf')
        if r == 0:
            return 0
        return (self.whites + (4 * self.wQueens)) - (self.blacks + (4 * self.bQueens))

    def posibleTakes(self, col=-1, row=-1):
        takes = []
        enemies = []
        if self.turn:
            enemies = [2, 4]
            allies = [1, 3]
        else:
            enemies = [1, 3]
            allies = [2, 4]

        def checkTakes(col, row):
            piece = self.board[col][row]
            if (piece in [3, 4] or self.turn) and piece in allies:
                if col - 2 >= 0 and row - 2 >= 0 and self.board[col - 1][row - 1] in enemies and self.board[col - 2][row - 2] == 0:
                    takes.append([col, row, col - 2, row - 2])
                if col + 2 < 8 and row - 2 >= 0 and self.board[col + 1][row - 1] in enemies and self.board[col + 2][row - 2] == 0:
                    takes.append([col, row, col + 2, row - 2])
            if (piece in [3, 4] or not self.turn) and self.board[col][row] in allies:
                if col - 2 >= 0 and row + 2 < 8 and self.board[col - 1][row + 1] in enemies and self.board[col - 2][row + 2] == 0:
                    takes.append([col, row, col - 2, row + 2])
                if col + 2 < 8 and row + 2 < 8 and self.board[col + 1][row + 1] in enemies and self.board[col + 2][row + 2] == 0:
                    takes.append([col, row, col + 2, row + 2])

        if col == -1:
            for row in range(8):
                for col in range(8):
                    checkTakes(col, row)
        else:
            checkTakes(col, row)

        multitakes = list()
        for take in takes:
            self.play(take, 0, 1)
            newTakes = self.posibleTakes(take[2], take[3])
            for newTake in newTakes:
                multitakes.append(take + [newTake[2], newTake[3]])
            self.undo(True)
        final = multitakes + takes
        return final

    def posibleMoves(self):
        moves = []
        allies = []
        if self.turn:
            allies = [1, 3]
        else:
            allies = [2, 4]

        for row in range(8):
            for col in range(8):
                piece = self.board[col][row]
                if (piece in [3, 4] or self.turn) and piece in allies:
                    if col - 1 >= 0 and row - 1 >= 0:
                        if self.board[col - 1][row - 1] == 0:
                            moves.append([col, row, col - 1, row - 1])
                    if col + 1 < 8 and row - 1 >= 0:
                        if self.board[col + 1][row - 1] == 0:
                            moves.append([col, row, col + 1, row - 1])
                if (piece in [3, 4] or not self.turn) and self.board[col][row] in allies:
                    if col - 1 >= 0 and row + 1 < 8:
                        if self.board[col - 1][row + 1] == 0:
                            moves.append([col, row, col - 1, row + 1])
                    if col + 1 < 8 and row + 1 < 8:
                        if self.board[col + 1][row + 1] == 0:
                            moves.append([col, row, col + 1, row + 1])
        return moves

    def undo(self, override=False):
        thisMove = self.historial[-1]

        def recur(move):
            self.board[move[0]][move[1]], self.board[move[2]][move[3]] = self.board[move[2]][move[3]], \
                                                                         self.board[move[0]][move[1]]
            if (move[4] != 0):
                self.board[(move[2] + move[0]) // 2][(move[1] + move[3]) // 2] = move[4]
                if move[4] % 2 == 1:
                    self.whites += 1
                else:
                    self.blacks += 1
            if move[5]:
                self.board[move[0]][move[1]] -= 2
                if self.board[move[0]][move[1]] == 1:
                    self.wQueens -= 1
                else:
                    self.bQueens -= 1

        if type(thisMove[0]) == list:
            for move in reversed(thisMove):
                recur(move)
        else:
            recur(thisMove)
        self.winner = -1

        if not override:
            self.turn = not self.turn
            self.moves = self.posibleMoves()
            self.takes = self.posibleTakes()

        self.historial.pop()

    def play(self, move, prof=0, override=0):
        if prof > 0:
            self.takes = self.posibleTakes()
            self.moves = self.posibleMoves()
        valid = False
        took = 0
        queen = False
        if override == 1 or (move in self.takes):
            self.board[move[0]][move[1]], self.board[move[2]][move[3]] = self.board[move[2]][move[3]], \
                                                                         self.board[move[0]][move[1]]
            self.board[(move[2] + move[0]) // 2][(move[1] + move[3]) // 2], took = took, \
                                                                                   self.board[(move[2] + move[0]) // 2][
                                                                                       (move[1] + move[3]) // 2]
            if self.turn:
                self.blacks -= 1
            else:
                self.whites -= 1
            valid = True
            if override == 0:
                self.emp = 0
        elif len(self.takes) == 0 and move in self.moves:
            self.board[move[0]][move[1]], self.board[move[2]][move[3]] = self.board[move[2]][move[3]], \
                                                                         self.board[move[0]][move[1]]
            valid = True
            if override == 0:
                self.emp += 1
        if valid:
            if self.board[move[2]][move[3]] == 1 and move[3] == 0:
                self.board[move[2]][move[3]] = 3
                self.wQueens += 1
                queen = True
            elif self.board[move[2]][move[3]] == 2 and move[3] == 7:
                self.board[move[2]][move[3]] = 4
                self.bQueens += 1
                queen = True
            thisPlay = move[:4]
            thisPlay += [took, queen]
            if len(move) > 4:
                move = move[2:]
                if prof == 0:
                    thisPlay = [thisPlay]
                thisPlay.append(self.play(move, prof + 1, override))
        if prof > 0:
            return thisPlay
        if valid:
            self.historial.append(thisPlay)
        return valid

    def translateInput(self, inp: str):
        inp = inp.split()
        for i in range(len(inp)):
            inp[i] = int(inp[i])
        return inp

    def getBoard(self) -> Board:
        matrix = [[0] * 8 for _ in range(8)]
        for y in range(8):
            for x in range(8):
                matrix[y][x] = self.board[x][y]
        return Board([], [], matrix)


