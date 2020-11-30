import curses
from curses import textpad

from lib import culour
from lib.exceptions import BreakMainLoop

from lib.sheet import Sheet

import time


class Game:
    def __init__(self, song):
        self.song = song

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

        while True:
            screen.timeout(int(sheet.bpm_delay * 1000))  # Millisecond

            start_ts = time.time()
            screen.clear()
            textpad.rectangle(screen, sheet_box[0][1], sheet_box[0][0], sheet_box[1][1], sheet_box[1][0])
            textpad.rectangle(screen, circuit_box[0][1], circuit_box[0][0], circuit_box[1][1], circuit_box[1][0])
            textpad.rectangle(screen, score_box[0][1], score_box[0][0], score_box[1][1], score_box[1][0])

            for idx, line in enumerate(sheet.render()):
                left_sheet_padding = (box_padding * 2 + ((screen_height - box_padding) - sheet.total_width) // 2) + 1
                top_sheet_padding = box_padding + idx
                culour.addstr(screen, top_sheet_padding, left_sheet_padding, line)
                screen.refresh()

            key = screen.getch()

            try:
                self.handle_key(key)
            except BreakMainLoop:
                break

            sheet.update_cursor()
            stop_ts = time.time()

            while stop_ts - start_ts < sheet.bpm_delay:
                screen.timeout(1)  # Millisecond
                key = screen.getch()
                try:
                    self.handle_key(key)
                except BreakMainLoop:
                    break
                stop_ts = time.time()

                # pause = min(sheet.bpm_delay, start_ts + sheet.bpm_delay - stop_ts)
                # stop_ts = time.time()
                # time.sleep(pause)

            # Sleep for the remaining time if a key have been pressed ?
            # screen.refresh()

    def handle_key(self, key):
        if key > -1:
            if key == ord("q"):
                raise BreakMainLoop
