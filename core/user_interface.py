'''
A class that manages the user interface
'''

from core.game import Game
from core.board import Player
from core.computer import Computer

import PySimpleGUI as sg

class UserInterface:
    def __init__(self, title: str, theme: str = "Default") -> None:
        sg.theme(theme)
        self.fonts = {
            "main": ("Consolas", 18), 
            "board": ("Arial", 24), 
            "sub_title": ("Consolas", 12)
        }

        self.game = Game()
        game_board = [
            [
                sg.Button(" ", size=(8, 4), key=(x, y), font=self.fonts["board"])
                for y in range(len(self.game.get_board()))
            ]
            for x in range(len(self.game.get_board()))
        ]

        layout = [
            [sg.Push(), sg.Text("TicTacToe", font=self.fonts["main"]), sg.Push()],
            [sg.Push(), sg.Text("", font=self.fonts["sub_title"], key="--SUB_TITLE--"), sg.Push()],
            game_board,
            [
                sg.Push(),
                sg.Button("Restart", key="--RESTART_BUTTON--", font=self.fonts["main"]),
                sg.Button("Change Mode", key="--MODE_BUTTON--", font=self.fonts["main"]),
                sg.Push(),
            ],
            [sg.Push(), sg.Text("", font=self.fonts["sub_title"], key="--MODE_TEXT--"), sg.Push()]
        ]

        self.window = sg.Window(title, layout)
        self.__has_shown_popup = False
        self.mode = None

    def run(self) -> None:
        self.mode = self.__startup()

        if not self.mode:
            return

        while True:
            event, values = self.window.read(timeout=10)
            if event in (sg.WIN_CLOSED, "Exit"):
                break
            
            if event == "--RESTART_BUTTON--":
                self.__restart_game()
            
            if event == "--MODE_BUTTON--":
                self.__restart_game()
                self.__swap_mode()

            self.window["--MODE_TEXT--"].update(f"Playing against {"the computer" if self.mode == "--PVE--" else "another person"}")

            if self.mode == "--PVE--":
                self.__play_pve(event)
            else:
                self.__play_pvp(event)
        
        self.__close()

    def __startup(self) -> str | None:
        layout = [
            [sg.Push(), sg.Text("How do you want to play?", font=self.fonts["main"]), sg.Push()],
            [
                sg.Button("Against the computer", font=self.fonts["sub_title"], key="--PVE--"), 
                sg.Button('Against another person', font=self.fonts["sub_title"], key="--PVP--")
            ]
        ]

        window = sg.Window(self.window.Title, layout)
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            return None
        
        window.close()

        return event
    
    def __swap_mode(self) -> None:
        if self.mode == "--PVE--":
            self.mode = "--PVP--"
        else:
            self.mode = "--PVE--"

    def __close(self) -> None:
        self.window.close()

    def __restart_game(self) -> None:
        self.game.restart()
        self.__has_shown_popup = False
        for i in range(len(self.game.get_board())):
            for j in range(len(self.game.get_board())):
                self.window[(i, j)].update(" ", button_color=sg.theme_button_color())

    def __play_pvp(self, event) -> None:
        current_player = self.game.get_current_player()

        if self.game.is_active():
            self.__play(current_player, event)
        else:
            self.__show_win_info()

    def __play_pve(self, event) -> None:
        ai = Computer(self.game.get_board(), Player.O)
        current_player = self.game.get_current_player()

        if self.game.is_active():
            if current_player == Player.X:
                self.__play(current_player, event)
            elif current_player == Player.O:
                row, col = ai.get_optimal_move()
                self.game.play(row, col)
                self.window[(row, col)].update(current_player.name)
        else:
            self.__show_win_info()

    def __show_win_info(self) -> None:
        winning_moves = self.game.get_winning_positions()
        winning_message = ("There is a draw" 
                            if not self.game.get_winner() else
                            f"The winner is {self.game.get_winner().name}")

        self.window["--SUB_TITLE--"].update(winning_message)
        for move in winning_moves:
            self.window[move].update(button_color="black on green")
        if not self.__has_shown_popup:
            sg.popup(winning_message, font=self.fonts["main"], title="Game Info")
            self.__has_shown_popup = True

    def __play(self, player: Player, event: (int, int)) -> None:
        self.window["--SUB_TITLE--"].update(f"It's {self.game.get_current_player().name}'s turn!")

        if not isinstance(event, tuple):
            return

        if self.window[event].get_text() != " ":
            return

        row, col = event
        self.game.play(row, col)
        self.window[(row, col)].update(player.name)