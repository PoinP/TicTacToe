"""
A class that manages the computer's AI
"""

from core.board import Board
from core.board import Player

import math


class Computer:
    def __init__(self, board: Board, player=Player.O) -> None:
        self.__board = board
        self.__player = player

    def get_optimal_move(self) -> (int, int):
        best_move = (-1, -1)
        best_score = -math.inf

        possible_moves = self.__get_available_moves()

        for row, col in possible_moves:
            self.__board.make_play(row, col, self.__player)
            score = self.__minimax(-math.inf, math.inf, False)
            self.__board.clear_pos(row, col)
            if score > best_score:
                best_score = score
                best_move = (row, col)

        return best_move

    def __get_available_moves(self) -> list[int, int]:
        def combinedZip(l1, l2):
            return [(x, y) for x in l1 for y in l2]

        moves = list(range(len(self.__board)))
        possible_moves = combinedZip(moves, moves)
        return list(
            filter(lambda x: self.__board.get_pos(x[0], x[1]) == " ", possible_moves)
        )

    def __minimax(self, alpha: int, beta: int, maximizing: bool, depth=0) -> float:
        winner = self.__board.get_winner()
        if self.__board.is_full() or winner:
            if not winner:
                return 0.0
            elif winner == self.__player:
                return 20.0 - depth
            else:
                return -20.0 + depth

        if maximizing:
            possible_moves = self.__get_available_moves()
            max_score = -math.inf

            for row, col in possible_moves:
                self.__board.make_play(row, col, self.__player)
                score = self.__minimax(alpha, beta, False, depth + 1)
                self.__board.clear_pos(row, col)

                max_score = max(max_score, score)
                alpha = max(alpha, max_score)
                if max_score >= beta:
                    break

            return max_score
        else:
            possible_moves = self.__get_available_moves()
            min_score = math.inf

            for row, col in possible_moves:
                self.__board.make_play(row, col, self.__get_opposite_player())
                score = self.__minimax(alpha, beta, True, depth + 1)
                self.__board.clear_pos(row, col)

                min_score = min(min_score, score)
                beta = min(beta, min_score)
                if min_score <= alpha:
                    break

            return min_score

    def __get_opposite_player(self) -> Player:
        return Player.X if self.__player == Player.O else Player.O
