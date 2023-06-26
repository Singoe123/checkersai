from models import Board, Piece, Game
from services import MinimaxService


class NextMoveService:
    # Next Move Service must not modify this constructor
    def __init__(self, minimax_service):
        self.__minimax_service: MinimaxService = minimax_service

    def make_ai_move(self, board: Board):
        objGame = Game(board)
        val, move = self.__minimax_service.minimax(objGame)
        objGame.play(move)

        return objGame.getBoard()