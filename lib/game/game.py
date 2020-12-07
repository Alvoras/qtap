import curses
import multiprocessing
from curses import textpad

from lib import culour
from lib.exceptions import BreakMainLoop
from lib.constants import FPS
from lib.game.input import handle_key

from lib.sheet import Sheet, SheetFinished
from lib.circuit.circuit import Circuit

import time
import lib.circuit.input as grid_input
from playsound import playsound

class Game:
    def __init__(self, song):
        self.song = song
        self.start_ts = time.time()
        self.stop_ts = 0
        self.score = 0
        self.failure = 0
        self.max_failure = 10
        self.score_step = 1
        self.music_player = None

    def stop_music(self):
        if self.music_player:
            self.music_player.terminate()

    def start(self):
        curses.wrapper(self.run)

    def run(self, screen):
        curses.curs_set(0)
        screen.nodelay(1)
        screen.keypad(1)

        box_padding = 2
        score_box_height = 10

        screen_height, screen_width = screen.getmaxyx()
        right_panel_left_padding = (screen_width // 3) + 1
        right_panel_right_padding = screen_width - 3

        sheet = Sheet(self.song, height=screen_height - box_padding * 4)
        circuit = Circuit(sheet.qbit_qty,
                          height=(screen_height - score_box_height) - box_padding,
                          width=((screen_width - box_padding) - ((box_padding * 2)+ right_panel_left_padding)))

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

        score_box = [[right_panel_left_padding, screen_height - score_box_height],
                     [right_panel_right_padding, screen_height - box_padding]]  # [[top_x, top_y], [bot_x, bot_y]]

        song_author_str = "Now playing : " + sheet.song.name + " - " + sheet.song.author

        screen.idcok(True)
        # screen.idlok(True)

        screen.timeout(int(1 / FPS * 1000))  # Millisecond
        sheet.ts()

        while True:
            # Clear screen
            screen.erase()

            # Draw windows
            textpad.rectangle(screen, sheet_box[0][1], sheet_box[0][0], sheet_box[1][1], sheet_box[1][0])
            textpad.rectangle(screen, circuit_box[0][1], circuit_box[0][0], circuit_box[1][1], circuit_box[1][0])
            textpad.rectangle(screen, score_box[0][1], score_box[0][0], score_box[1][1], score_box[1][0])

            top_sheet_padding_score = (screen_height - score_box_height) + 1
            culour.addstr(screen, top_sheet_padding_score, right_panel_left_padding + box_padding, song_author_str)
            culour.addstr(screen, top_sheet_padding_score + 1, right_panel_left_padding + box_padding,
                          "Score : " + str(self.score))

            # raise Exception(circuit.predict())
            predictions = list(circuit.predict())
            predicted_idx = predictions.index(max(predictions))
            if predictions.count(predicted_idx) > 1:
                predicted_idx = -1

            # Build sheet graphics line by line
            for idx, line in enumerate(sheet.render(predicted_idx)):
                if sheet.get_ready_done:
                    left_sheet_padding = (box_padding * 2 + ((screen_height - box_padding) - sheet.total_width) // 2) + 1
                else:
                    left_sheet_padding = (box_padding * 2 + ((screen_height - box_padding) - len(line)) // 2) + 4

                top_sheet_padding = box_padding + idx
                culour.addstr(screen, top_sheet_padding, left_sheet_padding, line)

            # Build circuit graphics line by line
            for idx, line in enumerate(circuit.render()):
                left_sheet_padding = box_padding + right_panel_left_padding
                top_sheet_padding = box_padding + idx
                culour.addstr(screen, top_sheet_padding, left_sheet_padding, line)

            key = screen.getch()

            try:
                grid_input.handle_input(circuit, key)
                handle_key(key)
            except BreakMainLoop:
                break

            # If the time delta between last loop and now is more than the BPM's delay, then forward the sheet
            if sheet.tick():
                try:
                    if sheet.has_value_to_compare():
                        measured = circuit.measure()
                        if sheet.compare(measured):
                            self.score += self.score_step
                        else:
                            self.failure += 1

                    sheet.update_cursor()

                    # Start playing the song
                    if sheet.steps - sheet.cursor == sheet.padding_height:
                        self.music_player = multiprocessing.Process(target=playsound, args=(self.song.music_file,))
                        self.music_player.start()

                    self.check_end()

                except SheetFinished:
                    raise

    def check_end(self):
        if self.failure >= self.max_failure:
            raise GameLost(self)


class GameLost(Exception):
    def __init__(self, game):
        super(GameLost, self).__init__()
        self.game = game

    def get_game(self):
        return self.game if self.game else None
