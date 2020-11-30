import os
import threading
from time import sleep

from lib.bar import Bar
from rich.console import Console

from lib.constants import FRETS_COLOR_MAP


class Sheet:
    def __init__(self, song, height=20):
        self.song = song
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
        # self.cursor = 0

    def update_cursor(self):
        self.cursor -= 1

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
                    with console.capture() as capture:
                        if "-" not in note:
                            console.print(f"[{color}]{note.rstrip()}[/{color}]", end="")
                        else:
                            console.print(note.rstrip(), end="")

                    lines[idx] += f"{capture.get()} "
            else:
                # Out of sheet bounds, we want to print blank lines to allow the sheet to scroll to the bottom
                lines.append(f"│ ---{' ' * self.qbit_qty}{(' ' * self.qbit_qty + ' ') * len(self.tracks)}│")

            lines[idx] += "│"

        lines.reverse()
        return lines

    def render(self):
        lines = self.make_tracks()
        lines += (self.bar.render())
        self.bar.update()
        lines = [line.replace("[1;", "[") for line in lines]
        return lines
        # return "\n".join(lines)
