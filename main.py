#!/bin/env python3
import os

from lib.exceptions import QuitGame
from lib.game.game import Game, GameLost
from lib.screens.failure_screen import show_failure_screen
from lib.sheet import SheetFinished
from colorama import init, deinit

from lib.menu import Menu,SongSelected
from lib.screens.title_screen import show_title_screen
from lib.screens.finish_screen import show_finish_screen

os.putenv("TERM", "xterm-256color")

show_title_screen()

init()
menu = Menu()

while True:
    try:
        menu.start()
    except SongSelected as song_exc:
        game = Game(song_exc.get_song())
    except QuitGame:
        break

    try:
        game.start()
    except SheetFinished:
        show_finish_screen(game)
    except GameLost:
        show_failure_screen(game)
    except QuitGame:
        break

deinit()

# sheet_file = "demo_3"
# sheet = Sheet(3, sheet_file, bpm=1)

# If a note is at the bottom of the screen, eval it
# Eval : measure probabilities from circuit, get goal (00,01...) from probabilities in the measure_tracks pool
#   Success :
#      Accelerate event loop
#      Visual feedback somewhere
#      Increase success score ?
#   Failure :
#      Add pause if eval failed ?
#      Decrement success score ?
#
# Eval loose condition
# Update sheet (cursor++)
# Update frets (bold on the next target note ?)
# Update circuit (clear if a note passed)
# Draw sheet
# Draw frets
# Draw circuit
