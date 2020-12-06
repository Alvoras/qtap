import curses
import os
from curses import textpad
from rich.console import Console

from lib import culour
from lib.constants import FPS
from lib.exceptions import BreakMainLoop, UnsupportedDifficultyMode, MissingSongSheet, QuitGame
from lib.sheet import Sheet
from lib.song import Song


class Menu:
    def __init__(self):
        self.songs_dir = "./songs"
        self.songs = []
        self.cursor = 0

        self.load_songs()

    def load_songs(self):
        cols, _ = os.get_terminal_size()

        for root, dirs, files in os.walk(self.songs_dir):
            for file in files:
                if file.endswith(".yml"):
                    for mode in ["easy", "hard"]:
                        try:
                            self.songs.append(Song(os.path.join(root, file), mode, root, cols))
                        except UnsupportedDifficultyMode:
                            continue
                        except MissingSongSheet as e:
                            print(e)
                            continue

    def start(self):
        curses.wrapper(self.run)

    def run(self, screen):
        curses.curs_set(0)
        screen.keypad(1)

        box_padding = 2
        score_box_height = 10

        screen_height, screen_width = screen.getmaxyx()

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

        cover_box = [[right_panel_left_padding, 1],
                       [right_panel_right_padding, screen_height - score_box_height]]  # [[top_x, top_y], [bot_x, bot_y]]

        score_box = [[right_panel_left_padding, screen_height - score_box_height],
                     [right_panel_right_padding, screen_height - box_padding]]  # [[top_x, top_y], [bot_x, bot_y]]

        screen.idcok(True)
        screen.idlok(True)

        sheet = Sheet(self.get_selected_song(), demo=True, height=screen_height - box_padding * 4)
        prev_cursor = self.cursor

        sheet.ts()
        screen.timeout(int(1 / FPS * 1000))  # Millisecond

        while True:
            if prev_cursor != self.cursor:
                sheet = Sheet(self.get_selected_song(), demo=True, height=screen_height - box_padding * 4)
                prev_cursor = self.cursor
            screen.timeout(int(sheet.bpm_delay * 1000))  # Millisecond

            screen.erase()
            textpad.rectangle(screen, sheet_box[0][1], sheet_box[0][0], sheet_box[1][1], sheet_box[1][0])
            textpad.rectangle(screen, cover_box[0][1], cover_box[0][0], cover_box[1][1], cover_box[1][0])
            textpad.rectangle(screen, score_box[0][1], score_box[0][0], score_box[1][1], score_box[1][0])

            for idx, line in enumerate(self.render()):
                top_sheet_padding = (screen_height - score_box_height) + idx + 1
                culour.addstr(screen, top_sheet_padding, right_panel_left_padding+box_padding, line)

            cover = self.get_selected_song_cover()
            if cover:
                for idx, line in enumerate(cover):
                    top_sheet_padding = box_padding + idx
                    screen.addstr(top_sheet_padding, (screen_width - box_padding) - (len(cover) * 2) - box_padding, line)

            for idx, line in enumerate(self.render_selected_song_meta()):
                top_sheet_padding = box_padding + idx
                culour.addstr(screen, top_sheet_padding, right_panel_left_padding + box_padding, line)

            for idx, line in enumerate(sheet.render_demo()):
                if sheet.demo_screen_done:
                    left_sheet_padding = (box_padding * 2 + ((screen_height - box_padding) - sheet.total_width) // 2) + 1
                else:
                    left_sheet_padding = (box_padding * 2 + ((screen_height - box_padding) - 43) // 2) + 4
                top_sheet_padding = box_padding + idx
                culour.addstr(screen, top_sheet_padding, left_sheet_padding, line)

            screen.refresh()

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
                raise SongSelected(self.songs[self.cursor])

    def render(self):
        songs_list = []
        console = Console()
        for song in self.songs:
            with console.capture() as capture:
                console.print(f"[green]●[/green]", end="") if song.mode == "easy" else console.print(f"[yellow]●[/yellow]", end="")
            dot = capture.get()

            songs_list.append(f"{dot} {song.name}")

        songs_list[self.cursor] = f"> {songs_list[self.cursor]}"
        return songs_list

    def render_selected_song_meta(self):
        song = self.get_selected_song()
        lines = [f"Name : {song.name}", f"Author : {song.author}", f"BPM : {song.bpm}", f"Difficulty : {song.mode}"]

        return lines

    def get_selected_song_cover(self):
        lines = self.get_selected_song().cover.splitlines()

        return [" ".join(c for c in line) for line in lines]

    def get_selected_song(self):
        return self.songs[self.cursor]


class SongSelected(Exception):
    def __init__(self, song):
        super(SongSelected, self).__init__()
        self.song = song

    def get_song(self):
        return self.song if self.song else None
