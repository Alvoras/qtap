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

MAX_MISSED = 10
SCORE_STEP = 1
ROTATION_INC = 2  # 2 == PI/2 (45°) increment | 4 == PI/4 (22.5)° increment | 8 == PI/8 (11.25°) increment

BIND_QUIT = "Quit"
BIND_MENU = "Menu"
BIND_X_GATE = "X gate"
BIND_Y_GATE = "Y gate"
BIND_Z_GATE = "Z gate"
BIND_H_GATE = "H gate"
BIND_S_GATE = "S gate"
BIND_SDG_GATE = "SDG gate"
BIND_T_GATE = "T gate"
BIND_TDG_GATE = "TDG gate"
BIND_ROTATE_LEFT = "Rotate left"
BIND_ROTATE_RIGHT = "Rotate right"
BIND_CONTROL_GATE = "Control gate"
BIND_MOVE_CONTROL_UP = "Move control UP"
BIND_MOVE_CONTROL_DOWN = "Move control DOWN"
BIND_DELETE_GATE = "Delete node"
BIND_CLEAN_CIRCUIT = "Clean circuit"


class Bindings:
    @staticmethod
    def values():
        return {
            BIND_X_GATE: "x",
            BIND_Y_GATE: "y",
            BIND_Z_GATE: "z",
            BIND_H_GATE: "h",
            BIND_S_GATE: "s",
            BIND_SDG_GATE: "S",
            BIND_T_GATE: "t",
            BIND_TDG_GATE: "T",
            BIND_ROTATE_LEFT: "a",
            BIND_ROTATE_RIGHT: "e",
            BIND_CONTROL_GATE: "c",
            BIND_MOVE_CONTROL_UP: "W",
            BIND_MOVE_CONTROL_DOWN: "w",
            BIND_DELETE_GATE: "SPACE",
            BIND_CLEAN_CIRCUIT: "r",
            BIND_QUIT: "q",
            BIND_MENU: "m"
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
