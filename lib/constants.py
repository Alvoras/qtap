from colorama import Fore

FRETS_COLOR_MAP = [
    Fore.RED,
    Fore.YELLOW,
    Fore.GREEN,
    Fore.BLUE,
    Fore.RED,
    Fore.YELLOW,
    Fore.GREEN,
    Fore.BLUE
]

MAX_COLUMNS = 4

MOVE_LEFT = 1
MOVE_RIGHT = 2
MOVE_UP = 3
MOVE_DOWN = 4
FPS = 30

NUM_SHOTS = 100


class Bindings:
    @staticmethod
    def values():
        return {
            "Back": "q",
            "Menu": "m",
            "X gate": "x",
            "Y gate": "y",
            "Z gate": "z",
            "H gate": "h",
            "S gate": "s",
            "SDG gate": "S",
            "T gate": "t",
            "TDG gate": "T",
            "Rotate left": "a",
            "Rotate right": "e",
            "Control gate": "c",
            "Move control up": "W",
            "Move control down": "w",
            "Delete gate": "SPACE"
        }

    @staticmethod
    def render(height):
        binds = Bindings.values()
        binds_keys = list(binds.keys())
        binds_vals = list(binds.values())
        lines = []
        longest = max(len(f"{key} : [{val}]") for key, val in binds.items())

        for col in range((len(binds) // height) + 1):
            left_padding = longest * col
            chunks = []
            for i in range(height):
                idx = i + (col * height)
                if idx >= len(binds):
                    break
                bind_string = f"{binds_keys[idx]} : [{binds_vals[idx]}]"
                chunks.append({left_padding: bind_string})

            lines.append(chunks)

        return lines
