from rich.console import Console

from lib.constants import FRETS_COLOR_MAP


class Bar:
    def __init__(self, qbit_qty):
        self.qbit_qty = qbit_qty
        self.tracks_qty = pow(qbit_qty, 2)
        self.tracks_measure = ["{0:b}".format(n).zfill(qbit_qty) for n in range(self.tracks_qty)]
        self.total_width = (len(self.tracks_measure) * qbit_qty) + (qbit_qty-1)

    def update(self):
        pass

    def make_frets(self):
        frets = []
        console = Console()
        for idx in range(self.tracks_qty):
            color = FRETS_COLOR_MAP[idx]
            with console.capture() as capture:
                console.print(f"[bold {color}]{'═' * self.qbit_qty}[/bold {color}] ", end="")

            frets.append(capture.get())

        return frets

    def make_track_ref(self):
        track_ref = []
        console = Console()
        for idx in range(self.tracks_qty):
            color = FRETS_COLOR_MAP[idx]
            with console.capture() as capture:
                console.print(f"[{color}]{self.tracks_measure[idx]}[/{color}] ", end="")

            track_ref.append(capture.get())

        return track_ref

    def render(self):
        lines = []
        lines.append(f"┌────{' ' * self.qbit_qty}{''.join(self.make_frets())}┐")
        lines.append(f"│░░░░{' ' * self.qbit_qty}{''.join(self.make_track_ref())}│")
        return lines

    def measure(self):
        pass
