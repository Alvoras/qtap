import sys
import time

from asciimatics.renderers import FigletText, Fire, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print, Stars
from asciimatics.exceptions import ResizeScreenError
from pyfiglet import Figlet
import qrng


def seconds_to_frame(sec):
    # A frame is 0.05s : one second is 20 frames (duration is in frame)
    return sec * 20


def animate(screen, game):
    scenes = []
    banner_text = game.song.name
    text = Figlet(font="banner", width=200).renderText(banner_text)
    width = max([len(x) for x in text.split("\n")])

    # top_padding = screen.height - 9
    top_padding = (screen.height // 3) - 3
    # fire_top_padding = top_padding + 8

    stars_bg = Stars(screen, 20, pattern="..[T]..   ...[H]...  ...[Z]...         ")

    effects = [
        # Print(screen,
        #       Fire(fire_top_padding, 80, text, 0.4, 30, screen.colours),
        #       0,
        #       speed=1,
        #       transparent=False),
        Print(screen,
              FigletText(banner_text, "banner"),
              top_padding, x=(screen.width - width) // 2 + 1,
              colour=Screen.COLOUR_BLACK,
              bg=Screen.COLOUR_BLACK,
              speed=1),
        Print(screen,
              FigletText(banner_text, "banner"),
              top_padding,
              colour=Screen.COLOUR_WHITE,
              bg=Screen.COLOUR_WHITE,
              speed=1),
        Print(screen,
              FigletText(banner_text, "banner"),
              top_padding,
              colour=Screen.COLOUR_WHITE,
              bg=Screen.COLOUR_WHITE,
              speed=1),
        stars_bg
    ]

    scenes.append(Scene(effects, duration=seconds_to_frame(2)))
    #
    # buttons_top_padding = screen.height - (screen.height // 3)
    #

    score_top_padding = ((screen.height // 3) * 2) - 3

    effects = [
        # Print(screen,
        #       Fire(fire_top_padding, 80, text, 0.4, 30, screen.colours),
        #       0,
        #       speed=1,
        #       transparent=False),
        Print(screen,
              FigletText(banner_text, "banner"),
              top_padding, x=(screen.width - width) // 2 + 1,
              colour=Screen.COLOUR_BLACK,
              bg=Screen.COLOUR_BLACK,
              speed=1),
        Print(screen,
              FigletText(banner_text, "banner"),
              top_padding,
              colour=Screen.COLOUR_WHITE,
              bg=Screen.COLOUR_WHITE,
              speed=1),
        Print(screen,
              FigletText(str(game.score), "banner"),
              score_top_padding, x=(screen.width - width) // 2 + 1,
              colour=Screen.COLOUR_BLACK,
              bg=Screen.COLOUR_BLACK,
              speed=1),
        Print(screen,
              FigletText(str(game.score), "banner"),
              score_top_padding,
              colour=Screen.COLOUR_WHITE,
              bg=Screen.COLOUR_WHITE,
              speed=1),
        stars_bg
    ]

    scenes.append(Scene(effects, duration=seconds_to_frame(4)))

    screen.play(scenes, repeat=False, stop_on_resize=True)


def show_finish_screen(game):
    try:
        Screen.wrapper(animate, arguments=[game])
    except ResizeScreenError:
        pass
