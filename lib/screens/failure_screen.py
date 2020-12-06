from random import randint, choice

from asciimatics.renderers import Plasma, FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print, Stars
from asciimatics.exceptions import ResizeScreenError


def seconds_to_frame(sec):
    # A frame is 0.05s : one second is 20 frames (duration is in frame)
    return sec * 20


class PlasmaScene(Scene):

    def __init__(self, screen, game):
        fonts = [
            "slant",
            "poison",
            "sblood",
            "banner",
            "banner3",
            "standard",
            "univers"
        ]
        font = choice(fonts)

        you_text = FigletText("YOU", font=font)
        lost_text = FigletText("LOST", font=font)
        continue_text = FigletText("Press any key to continue", font="term")

        self._screen = screen
        effects = [
            Print(screen,
                  Plasma(screen.height, screen.width, screen.colours),
                  0,
                  speed=1,
                  transparent=False),
        ]

        effects.append(Print(screen, continue_text,
                             screen.height - 3,
                             5,
                             speed=1
                             )
                       )

        effects.append(Print(screen, you_text,
                             (screen.height // 4) - you_text.max_height // 2,
                             (screen.width - you_text.max_width) // 2 + 1,
                             colour=Screen.COLOUR_BLACK,
                             start_frame=seconds_to_frame(2),
                             speed=1)
                       )

        effects.append(Print(screen, you_text,
                             (screen.height // 4) - you_text.max_height // 2,
                             (screen.width - you_text.max_width) // 2,
                             start_frame=seconds_to_frame(2),
                             speed=1)
                       )

        effects.append(Print(screen, lost_text,
                             ((screen.height // 4) * 2) - lost_text.max_height // 2,
                             (screen.width - lost_text.max_width) // 2 + 1,
                             colour=Screen.COLOUR_BLACK,
                             start_frame=seconds_to_frame(3),
                             speed=1)
                       )

        effects.append(Print(screen, lost_text,
                             ((screen.height // 4) * 2) - lost_text.max_height // 2,
                             (screen.width - lost_text.max_width) // 2,
                             start_frame=seconds_to_frame(3),
                             speed=1)
                       )

        super(PlasmaScene, self).__init__(effects, 200, clear=False)


def animate(screen, game):
    scenes = [PlasmaScene(screen, game)]
    screen.play(scenes, repeat=False, stop_on_resize=True)


def show_failure_screen(game):
    try:
        Screen.wrapper(animate, arguments=[game])
    except ResizeScreenError:
        pass
