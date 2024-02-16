'''
A class that manages the play of the game
'''

from core.board import Player
from core.board import Board


class Game:
    def __init__(self) -> None:
        self.__board = Board()
        self.__current_player = Player.X
        self.__is_game_active = True
        self.__winner: Player | None = None

    def is_active(self) -> bool:
        return self.__is_game_active

    def get_current_player(self) -> Player:
        return self.__current_player

    def get_winner(self) -> Player | None:
        return self.__winner

    def is_move_available(self, row, col) -> bool:
        return self.__board.get_pos(row, col) == " "

    def get_board(self) -> Board:
        return self.__board

    def get_winning_positions(self) -> list[(int, int)] | None:
        if not self.get_winner():
            return []

        return self.__board.get_winning_positions()

    def play(self, row: int, col: int) -> bool:
        if not self.is_active():
            return False

        if not self.is_move_available(row, col):
            return False

        self.__board.make_play(row, col, self.__current_player)
        self.__swap_players()

        self.__winner = self.__board.get_winner()

        if self.__winner or self.__board.is_full():
            self.__is_game_active = False

        return True

    def restart(self) -> None:
        self.__clear_board()
        self.__current_player = Player.X
        self.__is_game_active = True
        self.__winner = None

    def print_board(self) -> None:
        self.__board.print()

    def __swap_players(self) -> None:
        if self.__current_player == Player.X:
            self.__current_player = Player.O
        else:
            self.__current_player = Player.X

    def __clear_board(self) -> None:
        board_len = len(self.__board)

        for row in range(board_len):
            for col in range(board_len):
                self.__board.clear_pos(row, col)
