import curses
import multiprocessing
from curses import textpad

from lib import culour
from lib.exceptions import BreakMainLoop
from lib.constants import FPS, Bindings
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
        self.missed = 0
        self.max_missed = 10
        self.score_step = 1
        self.music_player = None
        self.last_measured = ""

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
        score_box_height = 3
        bindings_box_height = 10

        screen_height, screen_width = screen.getmaxyx()
        right_panel_left_padding = (screen_width // 3) + 1
        right_panel_right_padding = screen_width - 3

        sheet = Sheet(self.song, height=screen_height - box_padding * 4)
        circuit = Circuit(sheet.qbit_qty,
                          sheet.bar,
                          height=(screen_height - (score_box_height + bindings_box_height)) - box_padding,
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
                       [right_panel_right_padding, screen_height - (score_box_height + bindings_box_height)]]  # [[top_x, top_y], [bot_x, bot_y]]

        score_box = [[right_panel_left_padding, screen_height - (bindings_box_height + score_box_height)],
                     [right_panel_right_padding, screen_height - bindings_box_height]]  # [[top_x, top_y], [bot_x, bot_y]]

        bindings_box = [[right_panel_left_padding, screen_height - bindings_box_height],
                     [right_panel_right_padding, screen_height - box_padding]]  # [[top_x, top_y], [bot_x, bot_y]]

        song_author_str = f" Now playing : {sheet.song.name} - {sheet.song.author} "

        screen.idcok(True)
        # screen.idlok(True)

        screen.timeout(int(1 / FPS * 1000))  # Millisecond
        sheet.ts()
        screen.clear()

        while True:
            # Clear screen
            screen.erase()

            # Draw windows
            textpad.rectangle(screen, sheet_box[0][1], sheet_box[0][0], sheet_box[1][1], sheet_box[1][0])
            textpad.rectangle(screen, circuit_box[0][1], circuit_box[0][0], circuit_box[1][1], circuit_box[1][0])
            textpad.rectangle(screen, score_box[0][1], score_box[0][0], score_box[1][1], score_box[1][0])
            textpad.rectangle(screen, bindings_box[0][1], bindings_box[0][0], bindings_box[1][1], bindings_box[1][0])

            # Add score
            top_sheet_padding_score = screen_height - (score_box_height + bindings_box_height) + 1
            culour.addstr(screen, top_sheet_padding_score - 1, right_panel_left_padding + box_padding, song_author_str)
            culour.addstr(screen, top_sheet_padding_score, right_panel_left_padding + box_padding,
                          f"Score : {str(self.score)}")
            culour.addstr(screen, top_sheet_padding_score + 1, right_panel_left_padding + box_padding,
                          f"Missed : {self.missed}/{str(self.max_missed)}")

            # Add bindings
            binding_left_padding = right_panel_left_padding + box_padding
            for col in Bindings.render(bindings_box[1][1] - bindings_box[0][1] - 1):
                top_bindings_padding_score = bindings_box[0][1]
                for meta in col:
                    top_bindings_padding_score += 1
                    padding, line = list(meta.items())[0]

                    culour.addstr(screen, top_bindings_padding_score, binding_left_padding + padding, line)

            # Compute probabilities for the current circuit
            predictions = [int(round(abs(p))) for p in list(circuit.predict())]
            highest_proba = max(predictions)
            predicted_idx = predictions.index(highest_proba)
            if predictions.count(highest_proba) > 1:
                predicted_idx = -1

            # Build sheet graphics line by line
            for idx, line in enumerate(sheet.render(self.last_measured, predicted_idx)):
                if sheet.get_ready_done:
                    left_sheet_padding = (box_padding * 2 + ((screen_height - box_padding) - sheet.total_width) // 2) + 1
                else:
                    left_sheet_padding = (box_padding * 2 + ((screen_height - box_padding) - len(line)) // 2) + 4

                top_sheet_padding = box_padding + idx
                culour.addstr(screen, top_sheet_padding, left_sheet_padding, line)

            # Build circuit graphics line by line
            left_sheet_padding = box_padding + right_panel_left_padding
            for idx, line in enumerate(circuit.render(self.last_measured)):
                top_sheet_padding = box_padding + idx
                culour.addstr(screen, top_sheet_padding, left_sheet_padding, line)

            self.last_measured = ""

            key = screen.getch()

            try:
                grid_input.handle_input(circuit, key)
                handle_key(key)
            except BreakMainLoop:
                raise

            # If the time delta between last loop and now is more than the BPM's delay, then forward the sheet
            if sheet.tick():
                try:
                    if sheet.has_value_to_compare():
                        measured = circuit.measure()
                        self.last_measured = measured
                        if sheet.compare(measured):
                            self.score += self.score_step
                        else:
                            self.missed += 1

                    sheet.update_cursor()

                    # Start playing the song
                    if sheet.steps - sheet.cursor == sheet.padding_height:
                        if not self.song.music_file.endswith("_"):  # Do not play song if music_file is set to "_"
                            self.music_player = multiprocessing.Process(target=playsound, args=(self.song.music_file,))
                            self.music_player.start()

                    self.check_end()

                except SheetFinished:
                    raise

    def check_end(self):
        if self.song.miss and self.missed >= self.max_missed:
            raise GameLost(self)


class GameLost(Exception):
    def __init__(self, game):
        super(GameLost, self).__init__()
        self.game = game

    def get_game(self):
        return self.game if self.game else None
