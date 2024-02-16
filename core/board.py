"""
This class manages the TicTacToe Board
"""

from enum import Enum


class Player(Enum):
    X = 0
    O = 1  # noqa: E741


class Board:
    def __init__(self) -> None:
        BOARD_SIZE = 3
        self.__board = [[" " for y in range(BOARD_SIZE)] for x in range(BOARD_SIZE)]

    def __len__(self) -> int:
        return len(self.__board)

    def get_pos(self, row: int, col: int) -> str:
        if not self.__is_pos_valid(row, col):
            raise ValueError("Invalid Coordinates!")

        return self.__board[row][col]

    def clear_pos(self, row: int, col: int) -> None:
        if not self.__is_pos_valid(row, col):
            raise ValueError("Invalid Coordinates!")

        self.__board[row][col] = " "

    def make_play(self, row: int, col: int, player: Player) -> None:
        if not self.__is_pos_valid(row, col):
            raise ValueError("Invalid Coordinates!")

        self.__board[row][col] = "X" if player == Player.X else "O"

    def is_full(self) -> bool:
        return all([" " not in row for row in self.__board])

    def is_empty(self) -> bool:
        return not (self.is_full())

    def get_winner(self) -> Player | None:
        winner = (
            self.__check_rows()
            or self.__check_cols()
            or self.__check_main_diagonal()
            or self.__check_second_diagonal()
        )

        if not winner or next(iter(winner)) == " ":
            return None

        winning_player = next(iter(winner))
        return Player.X if winning_player == "X" else Player.O

    def get_winning_positions(self) -> list[(int, int)] | None:
        if self.__check_rows():
            for idx, row in enumerate(self.__board):
                if len(set(row)) == 1 and row[0] != " ":
                    return [(idx, col) for col in range(len(self))]

        if self.__check_cols():
            rotated_board = list(zip(*self.__board))
            for idx, row in enumerate(rotated_board):
                if len(set(row)) == 1 and row[0] != " ":
                    return [(col, idx) for col in range(len(rotated_board))]

        if self.__check_main_diagonal():
            board_len = len(self)
            return [(idx, idx) for idx in range(board_len)]

        if self.__check_second_diagonal():
            board_len = len(self)
            return [(board_len - idx - 1, idx) for idx in range(board_len)]

        return None

    def print(self) -> None:
        for row in self.__board:
            print(row)

    def __is_pos_valid(self, row: int, col: int) -> bool:
        board_length = len(self) - 1
        return 0 <= row <= board_length and 0 <= col <= board_length

    def __check_rows(self) -> set[str] | None:
        sets = [s for row in self.__board if len(s := set(row)) == 1 and row[0] != " "]
        return sets[0] if sets else None

    def __check_cols(self) -> set[str] | None:
        rotated_board = zip(*self.__board)
        sets = [s for row in rotated_board if len(s := set(row)) == 1 and row[0] != " "]
        return sets[0] if sets else None

    def __check_main_diagonal(self) -> set[str] | None:
        main_diagonal = [el[idx] for (idx, el) in enumerate(self.__board)]
        board_set = set(main_diagonal)
        return board_set if len(board_set) == 1 and main_diagonal[0] != " " else None

    def __check_second_diagonal(self) -> set[str] | None:
        board_length = len(self)
        second_diagonal = [el[board_length - idx - 1] for (idx, el) in enumerate(self.__board)]
        board_set = set(second_diagonal)
        return board_set if len(board_set) == 1 and second_diagonal[0] != " " else None
