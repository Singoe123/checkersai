from models import Game


class MinimaxService:
    def __init__(self, maxProf) -> None:
        self.maxProf = maxProf

    def minimax(self, objGame: Game, prof=0):
        bestMove = [0, 0, 0, 0]
        if prof > self.maxProf or objGame.winner != -1:
            return objGame.getEstado(), [0, 0, 0, 0]
        plays = objGame.takes
        if not plays:
            plays = objGame.moves
        if objGame.turn:
            value = float('-inf')
            for move in plays:
                ok = objGame.play(move, 0, 2)
                if ok:
                    objGame.turn = not objGame.turn
                    objGame.takes = objGame.posibleTakes()
                    objGame.moves = objGame.posibleMoves()
                    objGame.winner = objGame.checkWinner()
                    res, _ = self.minimax(objGame, prof + 1)
                    if res > value:
                        bestMove = move
                        value = res
                    objGame.undo()
            return value, bestMove
        else:
            value = float('inf')
            for move in plays:
                ok = objGame.play(move, 0, 2)
                if ok:
                    objGame.turn = not objGame.turn
                    objGame.takes = objGame.posibleTakes()
                    objGame.moves = objGame.posibleMoves()
                    objGame.winner = objGame.checkWinner()
                    res, _ = self.minimax(objGame, prof + 1)
                    if res < value:
                        bestMove = move
                        value = res
                    objGame.undo()
            return value, bestMove
