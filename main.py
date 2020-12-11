#!/bin/env python3
import os

from lib.exceptions import QuitGame, Back
from lib.game.game import Game, GameLost
from lib.screens.failure_screen import show_failure_screen
from lib.game.sheet import SheetFinished
from colorama import init, deinit

from lib.game.menu import Menu,SelectedSong
from lib.screens.title_screen import show_title_screen
from lib.screens.finish_screen import show_finish_screen

os.putenv("TERM", "xterm-256color")

show_title_screen()

init()
menu = Menu()

while True:
    game = None
    menu.songs = []

    try:
        menu.start()
    except SelectedSong as song_exc:
        game = Game(song_exc.get_song())
    except QuitGame:
        break

    try:
        game.start()
    except SheetFinished:
        game.stop_music()
        show_finish_screen(game)
    except GameLost:
        game.stop_music()
        show_failure_screen(game)
    except Back:
        game.stop_music()
    except QuitGame:
        game.stop_music()
        break

if game and game.music_player:
    game.stop_music()
    game.music_player.join()

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
