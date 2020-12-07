import time
from pyfiglet import Figlet

from lib.bar import Bar
from colorama import Style

from lib.constants import FRETS_COLOR_MAP


class Sheet:
    def __init__(self, song, demo=False, height=20):
        self.song = song

        self.start_ts = 0

        self.demo = demo
        self.demo_start_ts = None
        self.demo_screen_done = False
        # self.demo_counter = 0

        self.get_ready_done = False
        self.get_ready_counter = -4

        self.qbit_qty = 2 if self.song.mode == "easy" else 3
        self.bar = Bar(self.qbit_qty)

        self.render_buf = []

        self.height = height+2
        padding_duration = 5  # seconds
        self.padding_height = int((self.song.bpm / 60) * padding_duration)

        # We're using no fraction (== 4/4)
        self.bpm_delay = 1 / (self.song.bpm / 60)  # Delay in second between each beat (1 second / bpm / seconds in 1 minute)

        self.tracks = []
        for _ in self.bar.tracks_symbols:
            self.tracks.append([])

        self.total_width = 5 + self.qbit_qty + self.bar.total_width + 2
        empty_line = " ".join("-" * self.qbit_qty for _ in range(self.bar.tracks_qty))

        with open(self.song.sheet_file) as f:
            lines = f.readlines()
            for _ in range(self.padding_height):
                lines.insert(0, empty_line)

            lines.reverse()
            for line in lines:
                if line.startswith("#"):
                    continue
                notes = [note.rstrip() for note in line.split(" ")]
                for idx, note in enumerate(notes):
                    self.tracks[idx].append(note)

        self.steps = len(self.tracks[0])
        self.cursor = self.steps
        self.prev_cursor = 0

    def ts(self):
        self.start_ts = time.time()

    def tick(self):
        if time.time() - self.start_ts >= self.bpm_delay:
            self.ts()
            return True

        return False

    def check_end(self):
        if self.cursor < 0:
            if self.demo:
                self.cursor = self.steps
            else:
                self.signal_finished()

    def update_cursor(self):
        if self.demo and self.demo_screen_done:
            self.cursor -= 1
            self.demo_screen_done = False
            self.check_end()
        elif self.get_ready_done:
            self.cursor -= 1
            self.check_end()

    def has_value_to_compare(self):
        empty_symbol = "-"*self.qbit_qty

        if self.cursor >= len(self.tracks[0]):
            return False

        for i in range(len(self.tracks)):
            if self.tracks[i][self.cursor] != empty_symbol:
                return True

        return False

    def compare(self, measured):
        if self.cursor >= len(self.tracks[0]):
            return False

        for i in range(len(self.tracks)):
            if measured == self.tracks[i][self.cursor]:
                return True

        return False

    def make_tracks(self):
        lines = []
        for idx in range(self.height):
            # Within sheet bounds
            if self.cursor - (idx + 1) >= 0:
                if self.cursor - (idx + 1) > self.steps - self.padding_height:
                    lines.append(f"│ ---{' ' * self.qbit_qty}")
                else:
                    lines.append(f"│ {-((self.cursor - idx) - (self.steps - (self.padding_height - 1))):03}{' ' * self.qbit_qty}")
                for n, track in enumerate(self.tracks):
                    note = track[self.cursor - (idx + 1)]
                    color = FRETS_COLOR_MAP[n]
                    lines[idx] += f"{color}{note.rstrip()}{Style.RESET_ALL}" if "-" not in note else note.rstrip()
                    lines[idx] += " "
            else:
                # Out of sheet bounds, we want to print blank lines to allow the sheet to scroll to the bottom
                lines.append(f"│ ---{' ' * self.qbit_qty}{('-' * self.qbit_qty + ' ') * len(self.tracks)}")

            lines[idx] += "│"

        lines.reverse()
        return lines

    def render(self, predicted_idx=None):
        if self.cursor == self.prev_cursor:
            return self.render_buf
        if not self.demo:
            # Total duration of the countdown screen in frame
            max_frames = 55
            # Duration of one count in frame
            get_ready_period = 15
            # abs(55/15) = 3 steps in the countdown : 3,2,1

            half_text_height = 8 // 2

            get_ready_number = Figlet(font="banner").renderText(str(abs(self.get_ready_counter - max_frames)//get_ready_period)).splitlines()
            if not self.get_ready_done and self.get_ready_counter < max_frames + get_ready_period:
                if self.get_ready_counter > max_frames - get_ready_period:
                    get_ready_number = Figlet(font="banner").renderText("GO!").splitlines()
                if self.get_ready_counter > max_frames:
                    self.get_ready_done = True

                for i in range((self.height//2) - half_text_height):
                    get_ready_number.insert(0, "")

                self.get_ready_counter += 1
                return get_ready_number

        lines = self.make_tracks()

        lines += self.bar.render(predicted_idx)

        self.render_buf = lines
        self.prev_cursor = self.cursor

        return lines

    def render_demo(self):
        if not self.demo_start_ts:
            self.demo_start_ts = time.time()
        else:
            if time.time() - self.demo_start_ts >= 1:
                self.demo_screen_done = True

        demo_lines = f""" /$$$$$$$  /$$$$$$$$ /$$      /$$  /$$$$$$ 
| $$__  $$| $$_____/| $$$    /$$$ /$$__  $$
| $$  \ $$| $$      | $$$$  /$$$$| $$  \ $$
| $$  | $$| $$$$$   | $$ $$/$$ $$| $$  | $$
| $$  | $$| $$__/   | $$  $$$| $$| $$  | $$
| $$  | $$| $$      | $$\  $ | $$| $$  | $$
| $$$$$$$/| $$$$$$$$| $$ \/  | $$|  $$$$$$/
|_______/ |________/|__/     |__/ \______/ 
""".splitlines()

        for i in range(((self.height//2) - 4)):
            demo_lines.insert(0, "")
        return self.render() if self.demo_screen_done else demo_lines

    def signal_finished(self):
        raise SheetFinished(self)


class SheetFinished(Exception):
    def __init__(self, sheet):
        super(SheetFinished, self).__init__()
        self.sheet = sheet

    def get_sheet(self):
        return self.sheet if self.sheet else None
