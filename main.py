#!/bin/env python3
import curses
from curses import textpad

from lib import culour

from lib.sheet import Sheet
from lib.keyboard import BreakMainLoop, handle_key
import os


def main(screen):
    curses.curs_set(0)
    screen.nodelay(1)
    screen.keypad(1)

    box_padding = 2

    sh, sw = screen.getmaxyx()
    sheet_file = "demo"
    sheet = Sheet(2, sheet_file, height=sh - box_padding * 4, bpm=240)

    sheet_box = [[1, 2],
                 [sh - box_padding, sw // 3 - box_padding]]  # [[ul_y, ul_x], [dr_y, dr_x]]

    circuit_box = [[1, sw // 3],
                   [sh - box_padding, sw - 3]]  # [[ul_y, ul_x], [dr_y, dr_x]]

    screen.timeout(int(sheet.bpm_delay * 1000))  # Millisecond

    # screen.immedok(True)
    screen.idcok(True)
    screen.idlok(True)

    while True:
        # screen.erase()
        # screen.clearok(False)
        screen.clear()
        textpad.rectangle(screen, sheet_box[0][0], sheet_box[0][1], sheet_box[1][0], sheet_box[1][1])
        textpad.rectangle(screen, circuit_box[0][0], circuit_box[0][1], circuit_box[1][0], circuit_box[1][1])
        screen.border(0)

        for idx, line in enumerate(sheet.render()):
            left_sheet_padding = box_padding * 2 + (sheet.total_width // 2)
            top_sheet_padding = box_padding + idx
            culour.addstr(screen, top_sheet_padding, left_sheet_padding, line)
            screen.refresh()

        key = screen.getch()

        try:
            handle_key(key)
        except BreakMainLoop:
            break

        # culour.addstr(screen, (sh - box_padding) // 2, (sw // 3 - box_padding) // 2, str(sheet.cursor))

        sheet.update_cursor()
        # Sleep for the remaining time if a key have been pressed ?
        # screen.refresh()


os.putenv("TERM", "xterm-256color")
curses.wrapper(main)

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
