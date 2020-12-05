from colorama import Style

from lib.constants import FRETS_COLOR_MAP


class Bar:
    def __init__(self, qbit_qty):
        self.qbit_qty = qbit_qty
        self.tracks_qty = pow(2, qbit_qty)
        self.tracks_measure = ["{0:b}".format(n).zfill(qbit_qty) for n in range(self.tracks_qty)]
        self.total_width = (len(self.tracks_measure) * qbit_qty) + (qbit_qty-1)

    def update(self):
        pass

    def make_frets(self):
        frets = []
        for idx in range(self.tracks_qty):
            color = FRETS_COLOR_MAP[idx]
            frets.append(f"{Style.BRIGHT}{color}{'═' * self.qbit_qty}{Style.RESET_ALL} ")

        return frets

    def make_track_ref(self):
        track_ref = []
        for idx in range(self.tracks_qty):
            color = FRETS_COLOR_MAP[idx]
            track_ref.append(f"{Style.BRIGHT}{color}{self.tracks_measure[idx]}{Style.RESET_ALL} ")

        return track_ref

    def render(self):
        lines = []
        lines.append(f"┌────{' ' * self.qbit_qty}{''.join(self.make_frets())}┐")
        lines.append(f"│░░░░{' ' * self.qbit_qty}{''.join(self.make_track_ref())}│")
        return lines

    def measure(self):
        pass
