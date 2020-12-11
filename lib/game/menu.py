import curses
import os
from curses import textpad
from colorama import Fore, Style

from lib.display import culour
from lib.utils.constants import FPS
from lib.utils.exceptions import BreakMainLoop, UnsupportedDifficultyMode, MissingSongSheet, QuitGame
from lib.game.sheet import Sheet
from lib.game.song import Song


class Menu:
    def __init__(self):
        self.songs_dir = "./songs"
        self.songs = []
        self.cursor = 0
        self.box_padding = 2
        self.song_box_height = 10
        self.cover_box = 0
        self.real_cover_box_width = 0
        self.real_cover_box_height = 0
        self.song_list_height = self.song_box_height - (self.box_padding*2) + 1
        self.list_offset = 0

    def load_songs(self):
        for root, dirs, files in os.walk(self.songs_dir):
            for file in files:
                if file == "meta.yml":
                    for mode in ["easy", "hard"]:
                        for qbit_qty in [2, 3]:
                            try:
                                self.songs.append(Song(os.path.join(root, file), mode, qbit_qty, root, self.real_cover_box_width, self.real_cover_box_height))
                            except UnsupportedDifficultyMode:
                                continue
                            except MissingSongSheet as e:
                                # print(e)
                                continue

    def start(self):
        curses.wrapper(self.run)

    def run(self, screen):

        screen_height, screen_width = screen.getmaxyx()
        term_width, term_height = os.get_terminal_size()

        right_panel_left_padding = (screen_width // 3) + 1
        right_panel_right_padding = screen_width - 3

        self.cover_box = right_panel_left_padding - right_panel_right_padding
        self.real_cover_box_width = ((term_width // 3) + 1) - (term_width - 3)
        self.real_cover_box_height = screen_height - self.song_box_height - (self.box_padding*2)

        # Starts at 0,0 (top - left) :
        # ===
        # top_x,top_y -> x - - - - -
        #                  - - - - - -
        #                  - - - - - -
        #                  - - - - - x <- bot_x, bot_y

        sheet_box = [[2, 1],
                     [screen_width // 3 - (self.box_padding - 1), screen_height - self.box_padding]]  # [[top_x, top_y], [bot_x, bot_y]]

        cover_box = [[right_panel_left_padding, 1],
                       [right_panel_right_padding, screen_height - self.song_box_height]]  # [[top_x, top_y], [bot_x, bot_y]]

        song_box = [[right_panel_left_padding, screen_height - self.song_box_height],
                     [right_panel_right_padding, screen_height - self.box_padding]]  # [[top_x, top_y], [bot_x, bot_y]]

        self.load_songs()

        curses.curs_set(0)
        screen.keypad(1)

        screen.idcok(True)
        # screen.idlok(True)

        sheet = Sheet(self.get_selected_song(), demo=True, height=screen_height - self.box_padding * 4)
        prev_cursor = self.cursor

        sheet.ts()
        screen.timeout(int(1 / FPS * 1000))  # Millisecond

        while True:
            if prev_cursor != self.cursor:
                sheet = Sheet(self.get_selected_song(), demo=True, height=screen_height - self.box_padding * 4)
                prev_cursor = self.cursor
            screen.timeout(int(sheet.bpm_delay * 1000))  # Millisecond

            screen.erase()
            textpad.rectangle(screen, sheet_box[0][1], sheet_box[0][0], sheet_box[1][1], sheet_box[1][0])
            textpad.rectangle(screen, cover_box[0][1], cover_box[0][0], cover_box[1][1], cover_box[1][0])
            textpad.rectangle(screen, song_box[0][1], song_box[0][0], song_box[1][1], song_box[1][0])

            culour.addstr(screen, screen_height - self.song_box_height, right_panel_left_padding + 1, f' Press "Enter" to select a song ')

            for idx, line in enumerate(self.render()):
                top_sheet_padding = (screen_height - self.song_box_height) + idx + 1
                culour.addstr(screen, top_sheet_padding, right_panel_left_padding + self.box_padding, line)

            cover = self.get_selected_song_cover()
            if cover:
                for idx, line in enumerate(cover):
                    top_sheet_padding = self.box_padding + idx
                    screen.addstr(top_sheet_padding, (screen_width - self.box_padding) - (len(cover) * 2) - self.box_padding, line)

            for idx, line in enumerate(self.render_selected_song_meta()):
                top_sheet_padding = self.box_padding + idx
                culour.addstr(screen, top_sheet_padding, right_panel_left_padding + self.box_padding, line)

            for idx, line in enumerate(sheet.render_demo()):
                if sheet.demo_screen_done:
                    left_sheet_padding = (self.box_padding * 2 + ((screen_height - self.box_padding) - sheet.total_width) // 2) + 1
                else:
                    left_sheet_padding = (self.box_padding * 2 + ((screen_height - self.box_padding) - 43) // 2) + 4
                top_sheet_padding = self.box_padding + idx
                culour.addstr(screen, top_sheet_padding, left_sheet_padding, line)

            # screen.refresh()

            key = screen.getch()

            try:
                self.handle_key(key)
            except BreakMainLoop:
                break

            if sheet.tick():
                sheet.update_cursor()

    def handle_key(self, key):
        if key > -1:
            if key == ord("q"):
                raise QuitGame
            if key == curses.KEY_DOWN:
                if self.cursor < len(self.songs) - 1:
                    self.cursor += 1
            if key == curses.KEY_UP:
                if self.cursor > 0:
                    self.cursor -= 1
            if key == ord("\n"):
                raise SelectedSong(self.songs[self.cursor])

    def render(self):
        songs_list = []
        max_offset = self.song_list_height // 2
        offset = self.cursor - max_offset if self.cursor - max_offset >= 0 else 0
        songs_to_display = self.songs[offset : self.song_list_height + offset]
        screen_cursor = self.cursor if self.cursor < max_offset else max_offset

        for idx, song in enumerate(songs_to_display):
            dot = f"{Fore.GREEN}●{Style.RESET_ALL}" if song.mode == "easy" else f"{Fore.YELLOW}●{Style.RESET_ALL}"

            if idx == screen_cursor:
                songs_list.append(f"[{dot} {song.name} ({str(song.qbit_qty)}, {song.mode})]")
            else:
                songs_list.append(f" {dot} {song.name} ({str(song.qbit_qty)}, {song.mode})")

        return songs_list

    def render_selected_song_meta(self):
        song = self.get_selected_song()
        difficulty = f"{Fore.GREEN}{song.mode}{Style.RESET_ALL}" if song.mode == "easy" else f"{Fore.YELLOW}{song.mode}{Style.RESET_ALL}"
        lines = [f"Name : {song.name}", f"Author : {song.author}", f"BPM : {song.bpm}", f"Difficulty : {difficulty}", f"Qbits: {str(song.qbit_qty)}"]

        return lines

    def get_selected_song_cover(self):
        return self.get_selected_song().cover

    def get_selected_song(self):
        return self.songs[self.cursor]


class SelectedSong(Exception):
    def __init__(self, song):
        super(SelectedSong, self).__init__()
        self.song = song

    def get_song(self):
        return self.song if self.song else None
