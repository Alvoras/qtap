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


def animate(screen):
    scenes = []
    banner_text = "QTAP"
    text = Figlet(font="banner", width=200).renderText(banner_text)
    width = max([len(x) for x in text.split("\n")])

    # top_padding = screen.height - 9
    top_padding = (screen.height // 2) - 3
    # fire_top_padding = top_padding + 8

    max_rng = (screen.width + screen.height) // 2
    qrng.set_provider_as_IBMQ('')
    qrng.set_backend()
    rng = qrng.get_random_int((max_rng // 3) * 2, max_rng)

    stars_bg = Stars(screen, rng, pattern="..[T]..   ...[H]...  ...[Z]...         ")

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
        stars_bg
    ]

    scenes.append(Scene(effects, duration=seconds_to_frame(2)))
    #
    # buttons_top_padding = screen.height - (screen.height // 3)
    #
    # effects = [
    #     Print(screen,
    #           FigletText(banner_text, "banner"),
    #           buttons_top_padding,
    #           x=width,
    #           colour=Screen.COLOUR_WHITE,
    #           bg=Screen.COLOUR_WHITE,
    #           speed=1),
    #     Print(screen,
    #           FigletText(banner_text, "banner"),
    #           buttons_top_padding,
    #           x=screen.width - (screen.width // 3),
    #           colour=Screen.COLOUR_WHITE,
    #           bg=Screen.COLOUR_WHITE,
    #           speed=1),
    #     stars_bg
    # ]
    #
    # scenes.append(Scene(effects, -1))

    screen.play(scenes, repeat=False, stop_on_resize=True)


def show_title_screen():
    try:
        Screen.wrapper(animate)
    except ResizeScreenError:
        pass
