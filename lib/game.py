import curses
from curses import textpad

from lib import culour
from lib.exceptions import BreakMainLoop, SheetFinished, QuitGame
from lib.constants import FPS

from lib.sheet import Sheet

import time


class Game:
    def __init__(self, song):
        self.song = song
        self.start_ts = time.time()
        self.stop_ts = 0

    def start(self):
        curses.wrapper(self.run)

    def run(self, screen):
        curses.curs_set(0)
        screen.nodelay(1)
        screen.keypad(1)

        box_padding = 2
        score_box_height = 10

        screen_height, screen_width = screen.getmaxyx()

        sheet = Sheet(self.song, height=screen_height - box_padding * 4)

        right_panel_left_padding = (screen_width // 3) + 1
        right_panel_right_padding = screen_width - 3

        # Starts at 0,0 (top - left) :
        # ===
        # top_x,top_y -> x - - - - -
        #                  - - - - - -
        #                  - - - - - -
        #                  - - - - - x <- bot_x, bot_y

        sheet_box = [[2, 1],
                     [screen_width // 3 - (box_padding - 1), screen_height - box_padding]]  # [[top_x, top_y], [bot_x, bot_y]]

        circuit_box = [[right_panel_left_padding, 1],
                       [right_panel_right_padding, screen_height - score_box_height]]  # [[top_x, top_y], [bot_x, bot_y]]

        score_box = [[right_panel_left_padding, (screen_height - score_box_height)],
                     [right_panel_right_padding, screen_height - box_padding]]  # [[top_x, top_y], [bot_x, bot_y]]

        screen.idcok(True)
        screen.idlok(True)

        screen.timeout(int(1 / FPS * 1000))  # Millisecond
        sheet.ts()

        while True:
            # Clear screen
            screen.clear()

            # Draw windows
            textpad.rectangle(screen, sheet_box[0][1], sheet_box[0][0], sheet_box[1][1], sheet_box[1][0])
            textpad.rectangle(screen, circuit_box[0][1], circuit_box[0][0], circuit_box[1][1], circuit_box[1][0])
            textpad.rectangle(screen, score_box[0][1], score_box[0][0], score_box[1][1], score_box[1][0])

            # Build sheet graphics line by line
            for idx, line in enumerate(sheet.render()):
                if sheet.get_ready_done:
                    left_sheet_padding = (box_padding * 2 + ((screen_height - box_padding) - sheet.total_width) // 2) + 1
                else:
                    left_sheet_padding = (box_padding * 2 + ((screen_height - box_padding) - len(line)) // 2) + 4

                top_sheet_padding = box_padding + idx
                culour.addstr(screen, top_sheet_padding, left_sheet_padding, line)

            # Flush built graphics to screen
            screen.refresh()

            key = screen.getch()

            try:
                self.handle_key(key)
            except BreakMainLoop:
                break

            # If the time delta between last loop and now is more than the BPM's delay, then forward the sheet
            if sheet.tick():
                try:
                    sheet.update_cursor()
                except SheetFinished:
                    pass
    #               goto end game

    def handle_key(self, key):
        if key > -1:
            if key == ord("q"):
                raise QuitGame
