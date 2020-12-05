import time
from pyfiglet import Figlet

from lib.bar import Bar
from colorama import Style
from rich.console import Console

from lib.constants import FRETS_COLOR_MAP
from lib.exceptions import SheetFinished


class Sheet:
    def __init__(self, song, demo=False, height=20):
        self.song = song

        self.start_ts = 0

        self.demo = demo
        self.demo_start_ts = None
        self.demo_screen_done = False
        self.demo_counter = 0

        self.get_ready_done = False
        self.get_ready_counter = -4

        self.qbit_qty = 2 if self.song.mode == "easy" else 3
        self.bar = Bar(self.qbit_qty)

        self.height = height+2

        # We're using no fraction (== 4/4)
        self.bpm_delay = 1 / (self.song.bpm / 60)  # Delay in second between each beat (1 second / bpm / seconds in 1 minute)

        self.tracks = []
        for _ in self.bar.tracks_measure:
            self.tracks.append([])

        self.total_width = 5 + self.qbit_qty + self.bar.total_width + 2

        with open(self.song.sheet_file) as f:
            lines = f.readlines()
            lines.reverse()
            for line in lines:
                if line.startswith("#"):
                    continue
                notes = [note.rstrip() for note in line.split(" ")]
                for idx, note in enumerate(notes):
                    self.tracks[idx].append(note)

        self.steps = len(self.tracks[0])
        self.cursor = self.steps

    def ts(self):
        self.start_ts = time.time()

    def tick(self):
        if time.time() - self.start_ts >= self.bpm_delay:
            self.ts()
            return True

        return False

    def check_end(self):
        if self.cursor < (0 - self.height):
            raise SheetFinished

    def update_cursor(self):
        if self.demo and self.demo_screen_done:
            self.cursor -= 1
            self.check_end()
        elif self.get_ready_done:
            self.cursor -= 1
            self.check_end()

    def make_tracks(self):
        lines = []
        console = Console()
        for idx in range(self.height):
            # Within sheet bounds
            if self.cursor - (idx + 1) >= 0:
                lines.append(f"│ {-((self.cursor - idx) - self.steps):03}{' ' * self.qbit_qty}")
                for n, track in enumerate(self.tracks):
                    note = track[self.cursor - (idx + 1)]
                    color = FRETS_COLOR_MAP[n]
                    lines[idx] += f"{color}{note.rstrip()}{Style.RESET_ALL}" if "-" not in note else note.rstrip()
                    lines[idx] += " "
            else:
                # Out of sheet bounds, we want to print blank lines to allow the sheet to scroll to the bottom
                lines.append(f"│ ---{' ' * self.qbit_qty}{(' ' * self.qbit_qty + ' ') * len(self.tracks)}│")

            lines[idx] += "│"

        lines.reverse()
        return lines

    def render(self):
        if not self.demo:
            # Total duration of the countdown screen in frame
            max_frames = 90
            # Duration of one count in frame
            get_ready_period = 15
            # 90/15 = 6 steps in the countdown : 5,4,3,2,1,0

            half_text_height = 8 // 2

            get_ready_number = Figlet(font="banner").renderText(str(abs(self.get_ready_counter - max_frames)//get_ready_period - 1)).splitlines()
            if not self.get_ready_done and self.get_ready_counter < max_frames + get_ready_period:
                self.get_ready_counter += 1
                if self.get_ready_counter > max_frames - get_ready_period:
                    get_ready_number = Figlet(font="banner").renderText("GO!").splitlines()
                if self.get_ready_counter > max_frames:
                    self.get_ready_done = True

                for i in range((self.height//2) - half_text_height):
                    get_ready_number.insert(0, "")

                return get_ready_number

        lines = self.make_tracks()
        lines += (self.bar.render())
        self.bar.update()
        lines = [line.replace("[1;", "[") for line in lines]
        return lines

    def render_demo(self):
        if not self.demo_start_ts:
            self.demo_start_ts = time.time()
        else:
            if time.time() - self.demo_start_ts >= 1:
                self.demo_screen_done = True
            # elif self.demo_counter < 6:
            #     self.demo_counter += 1

        demo_lines = f""" /$$$$$$$  /$$$$$$$$ /$$      /$$  /$$$$$$ 
| $$__  $$| $$_____/| $$$    /$$$ /$$__  $$
| $$  \ $$| $$      | $$$$  /$$$$| $$  \ $$
| $$  | $$| $$$$$   | $$ $$/$$ $$| $$  | $$
| $$  | $$| $$__/   | $$  $$$| $$| $$  | $$
| $$  | $$| $$      | $$\  $ | $$| $$  | $$
| $$$$$$$/| $$$$$$$$| $$ \/  | $$|  $$$$$$/
|_______/ |________/|__/     |__/ \______/ 
""".splitlines()

        # for i in range(((self.height//2) - 4) - self.demo_counter//2):
        for i in range(((self.height//2) - 4) - self.demo_counter//2):
            demo_lines.insert(0, "")
        return self.render() if self.demo_screen_done else demo_lines
