import os
import threading
from time import sleep

from lib.bar import Bar


class Sheet:
    sheets_dir = "sheets"
    sheets_ext = ".qtap"

    def __init__(self, qbit_qty, sheet_file, height=20, bpm=120):
        self.qbit_qty = qbit_qty
        self.bar = Bar(qbit_qty)

        self.height = height+2
        self.sheet_file = sheet_file

        path = os.path.join(self.sheets_dir, self.sheet_file)
        self.sheet_path = path + self.sheets_ext if not self.sheet_file.endswith(self.sheets_ext) else path

        # We're using no fraction (== 4/4)
        self.bpm = bpm
        self.bpm_delay = 1 / (self.bpm / 60)  # Delay in second between each beat (1 second / bpm / seconds in 1 minute)

        self.tracks = []
        for _ in self.bar.tracks_measure:
            self.tracks.append([])

        self.total_width = 5 + self.qbit_qty + self.bar.total_width + 2

        with open(self.sheet_path) as f:
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
        # self.cursor = 0

    def update_cursor(self):
        self.cursor -= 1

    def start(self):
        thread = threading.Thread(target=self.run)
        thread.start()

    def make_tracks(self):
        lines = []
        for idx in range(self.height):
            # Within sheet bounds
            if self.cursor - (idx + 1) >= 0:
                lines.append(f"│ {-((self.cursor - idx) - self.steps):03}{' ' * self.qbit_qty}")
                for track in self.tracks:
                    note = track[self.cursor - (idx + 1)]
                    lines[idx] += f"{note.rstrip()} "

                lines[idx] += "│"
            else:
                # Out of sheet bounds, we want to print blank lines to allow the sheet to scroll to the bottom
                lines.append(f"│ ---{' ' * self.qbit_qty}{(' ' * self.qbit_qty + ' ') * len(self.tracks)}│")

        lines.reverse()
        return lines

    def render(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        lines = self.make_tracks()
        lines += (self.bar.render())
        self.bar.update()
        lines = [line.replace("[1;", "[") for line in lines]
        return lines
        # return "\n".join(lines)

    def run(self):
        while self.cursor >= 0:
            print(self.render())
            self.cursor -= 1
            sleep(self.bpm_delay)
            # input()
