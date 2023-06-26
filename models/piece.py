
class Piece:
    def __init__(self, is_queen: bool, x_coordinate: int, y_coordinate: int, is_ai_piece: bool):
        self.__is_queen = is_queen
        self.__x_coordinate = x_coordinate
        self.__y_coordinate = y_coordinate
        self.__is_ai_piece = is_ai_piece

    def set_is_queen(self, new_state: bool):
        self.__is_queen = new_state

    def set_coordinates(self, x_coordinate: int, y_coordinate: int):
        self.__x_coordinate = x_coordinate
        self.__y_coordinate = y_coordinate

    def set_x_coordinate(self, x_coordinate: int):
        self.__x_coordinate = x_coordinate

    def set_y_coordinate(self, y_coordinate: int):
        self.__y_coordinate = y_coordinate

    def get_is_queen(self) -> bool:
        return self.__is_queen

    def get_coordinates(self) -> tuple[int, int]:
        return self.__x_coordinate, self.__y_coordinate

    def get_x_coordinate(self) -> int:
        return self.__x_coordinate

    def get_y_coordinate(self) -> int:
        return self.__y_coordinate

    # For print(piece) functionality, where piece is an instance of Piece
    def __str__(self) -> str:
        piece_color = "\033[96m" if self.__is_ai_piece else "\033[92m"
        character = "X" if self.__is_ai_piece else "O"
        return f"{piece_color}{character}\033[0m"
