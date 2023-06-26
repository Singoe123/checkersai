from models import Board, Piece
from services import MinimaxService, NextMoveService 


def run_test():
    # Create next move and minimax service
    minimax_service = MinimaxService(5)
    next_move_service = NextMoveService(minimax_service)

    matrix = [[0] * 8 for _ in range(8)]
    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                matrix[row][col] = 2;
    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:
                matrix[row][col] = 1;
    board = Board(board=matrix)

    # Print initial state on CLI
    print("Initial State:")
    print(board)

    # AI makes the best move
    board = next_move_service.make_ai_move(board)

    # Print final state on CLI
    print("Final State:")
    print(board)

if __name__ == "__main__":
    run_test()
    input()
