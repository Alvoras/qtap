from colorama import Style, Back

from lib.constants import FRETS_COLOR_MAP


class Bar:
    def __init__(self, qbit_qty):
        self.qbit_qty = qbit_qty
        self.tracks_qty = pow(2, qbit_qty)
        self.tracks_symbols = ["{0:b}".format(n).zfill(qbit_qty) for n in range(self.tracks_qty)]
        self.total_width = (len(self.tracks_symbols) * qbit_qty) + (qbit_qty-1)

    def make_frets(self):
        frets = []
        for idx in range(self.tracks_qty):
            color = FRETS_COLOR_MAP[idx]
            frets.append(f"{Style.BRIGHT}{color}{'═' * self.qbit_qty}{Style.RESET_ALL} ")

        return frets

    def make_track_ref(self, last_measured):
        last_measured_keys = list(last_measured.keys())
        track_ref = []
        for idx in range(self.tracks_qty):
            color = FRETS_COLOR_MAP[idx]
            if self.tracks_symbols[idx] in last_measured_keys:
                track_ref.append(f"{Back.WHITE}{Style.BRIGHT}{color}{self.tracks_symbols[idx]}{Style.RESET_ALL}")
            else:
                track_ref.append(f"{Style.BRIGHT}{color}{self.tracks_symbols[idx]}{Style.RESET_ALL}")

        return track_ref

    def render(self, last_measured, predicted_idx):
        if predicted_idx is None:
            predicted = "░░░░"
        else:
            if predicted_idx == -1:
                predicted = "~"
            else:
                predicted = self.tracks_symbols[predicted_idx]
            predicted_color = FRETS_COLOR_MAP[predicted_idx]
            predicted = f"{Style.BRIGHT}{predicted_color}{predicted.center(4)}{Style.RESET_ALL}"

        lines = [f"┌────{' ' * self.qbit_qty}{''.join(self.make_frets())}┐",
                 f"│ {predicted}{' ' * (self.qbit_qty - 1)}{' '.join(self.make_track_ref(last_measured))} │"]

        return lines
