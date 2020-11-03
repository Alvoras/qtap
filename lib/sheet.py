import os
import threading
from time import sleep

MICROSEC = 1000000.0


class Sheet:
    sheets_dir = "sheets"
    sheets_ext = ".qtap"

    def __init__(self, qbit_qty, sheet_file, height=20, bpm=120):
        self.tracks = []
        self.qbit_qty = qbit_qty
        self.height = height
        self.sheet_file = sheet_file

        path = os.path.join(self.sheets_dir, self.sheet_file)
        self.sheet_path = path + self.sheets_ext if not self.sheet_file.endswith(self.sheets_ext) else path

        # We're using no fraction (== 4/4)
        self.bpm = bpm
        self.bpm_delay = 1 / (self.bpm / 60)  # Delay in second between each beat (1 second / bpm / seconds in 1 minute)

        self.tracks_measure = ["{0:b}".format(n).zfill(qbit_qty) for n in range(pow(qbit_qty, 2))]
        self.tracks = []
        for _ in self.tracks_measure:
            self.tracks.append([])

        with open(self.sheet_path) as f:
            lines = f.readlines()
            lines.reverse()
            for line in lines:
                if line.startswith("#"):
                    continue
                notes = [note.rstrip() for note in line.split(" ")]
                for idx, note in enumerate(notes):
                    self.tracks[idx].append(note)

        self.cursor = len(self.tracks[0])
        # self.cursor = 0

    def start(self):
        thread = threading.Thread(target=self.draw)
        thread.start()

    def draw(self):
        while self.cursor >= 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            lines = []
            for idx in range(self.height):
                if self.cursor - (idx + 1) >= 0:
                    lines.append(f"│ {(idx + self.height) - (self.cursor - self.height):03}{' ' * self.qbit_qty}")
                    for track in self.tracks:
                        note = track[self.cursor - (idx + 1)]
                        lines[idx] += f"{note.rstrip()} "

                    lines[idx] += "│"
                else:
                    lines.append(f"│ ---{' ' * self.qbit_qty}{(' ' * self.qbit_qty + ' ') * len(self.tracks_measure)}│")

            lines.reverse()

            lines.append(f"┌────{' ' * self.qbit_qty}{('═' * self.qbit_qty + ' ') * len(self.tracks_measure)}┐")
            lines.append(f"│░░░░{' ' * self.qbit_qty}{' '.join(self.tracks_measure)} │")
            print("\n".join(lines))
            self.cursor -= 1
            sleep(self.bpm_delay)
            # input()
