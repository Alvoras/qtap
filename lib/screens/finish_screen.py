from random import randint, choice

from asciimatics.particles import PalmFirework, StarFirework, SerpentFirework, RingFirework
from asciimatics.renderers import FigletText, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print, Stars
from asciimatics.exceptions import ResizeScreenError
from asciimatics.widgets import ListBox, Divider, Layout, Widget, Frame


def seconds_to_frame(sec):
    # A frame is 0.05s : one second is 20 frames (duration is in frame)
    return sec * 20


class ListView(Frame):
    def __init__(self, screen):
        super(ListView, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="Scoreboard")
        # Save off the model that accesses the contacts database.

        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            [])
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        self.fix()


def animate(screen, game):
    score_text = FigletText(f"Score : {game.score}", font='slant')
    song_text = Rainbow(screen, FigletText(game.song.name, font='slant'))
    failure_text = FigletText(f"Failure : {game.failure}", font='slant')
    continue_text = FigletText("Press any key to continue", font="term")

    scenes = []
    effects = [
        Stars(screen, screen.width)
    ]
    for _ in range(20):
        fireworks = [
            (PalmFirework, 25, 30),
            (PalmFirework, 25, 30),
            (StarFirework, 25, 35),
            (StarFirework, 25, 35),
            (StarFirework, 25, 35),
            (RingFirework, 20, 30),
            (SerpentFirework, 30, 35),
        ]
        firework, start, stop = choice(fireworks)
        effects.insert(
            1,
            firework(screen,
                     randint(0, screen.width),
                     randint(screen.height // 8, screen.height * 3 // 4),
                     randint(start, stop),
                     start_frame=randint(0, 250)),
        )

        effects.append(Print(screen, continue_text,
                             screen.height - 3,
                             5,
                             transparent=False,
                             speed=1,
                             )
                       )

        effects.append(Print(screen, continue_text,
                             screen.height - 3,
                             5,
                             transparent=False,
                             speed=1,
                             )
                       )

        effects.append(Print(screen, song_text,
                             (screen.height // 4) - 3,
                             (screen.width - song_text.max_width) // 2,
                             Screen.COLOUR_GREEN,
                             transparent=False,
                             speed=1,
                             start_frame=seconds_to_frame(1))
                       )
        effects.append(Print(screen, score_text,
                             ((screen.height // 4) * 2) - 3,
                             (screen.width - score_text.max_width) // 2,
                             transparent=False,
                             speed=1,
                             start_frame=seconds_to_frame(2))
                       )
        effects.append(Print(screen, failure_text,
                             ((screen.height // 4) * 3) - 3,
                             (screen.width - failure_text.max_width) // 2,
                             transparent=False,
                             speed=1,
                             start_frame=seconds_to_frame(3))
                       )

    # effects.append(Print(screen,
    #                      Rainbow(screen, FigletText("NEW YEAR!")),
    #                      screen.height // 2 + 1,
    #                      speed=1,
    #                      start_frame=100))
    scenes.append(Scene(effects, -1))
    # scenes.append(Scene([ListView(screen)], -1))

    screen.play(scenes, repeat=False, stop_on_resize=True)


# def animate(screen, game):
#     scenes = []
#     banner_text = game.song.name
#     text = Figlet(font="banner", width=200).renderText(banner_text)
#     width = max([len(x) for x in text.split("\n")])
#
#     # top_padding = screen.height - 9
#     top_padding = (screen.height // 3) - 3
#     # fire_top_padding = top_padding + 8
#
#     stars_bg = Stars(screen, 20, pattern="..[T]..   ...[H]...  ...[Z]...         ")
#
#     effects = [
#         # Print(screen,
#         #       Fire(fire_top_padding, 80, text, 0.4, 30, screen.colours),
#         #       0,
#         #       speed=1,
#         #       transparent=False),
#         Print(screen,
#               FigletText(banner_text, "banner"),
#               top_padding, x=(screen.width - width) // 2 + 1,
#               colour=Screen.COLOUR_BLACK,
#               bg=Screen.COLOUR_BLACK,
#               speed=1),
#         Print(screen,
#               FigletText(banner_text, "banner"),
#               top_padding,
#               colour=Screen.COLOUR_WHITE,
#               bg=Screen.COLOUR_WHITE,
#               speed=1),
#         Print(screen,
#               FigletText(banner_text, "banner"),
#               top_padding,
#               colour=Screen.COLOUR_WHITE,
#               bg=Screen.COLOUR_WHITE,
#               speed=1),
#         stars_bg
#     ]
#
#     scenes.append(Scene(effects, duration=seconds_to_frame(2)))
#     #
#     # buttons_top_padding = screen.height - (screen.height // 3)
#     #
#
#     score_top_padding = ((screen.height // 3) * 2) - 3
#
#     effects = [
#         # Print(screen,
#         #       Fire(fire_top_padding, 80, text, 0.4, 30, screen.colours),
#         #       0,
#         #       speed=1,
#         #       transparent=False),
#         Print(screen,
#               FigletText(banner_text, "banner"),
#               top_padding, x=(screen.width - width) // 2 + 1,
#               colour=Screen.COLOUR_BLACK,
#               bg=Screen.COLOUR_BLACK,
#               speed=1),
#         Print(screen,
#               FigletText(banner_text, "banner"),
#               top_padding,
#               colour=Screen.COLOUR_WHITE,
#               bg=Screen.COLOUR_WHITE,
#               speed=1),
#         Print(screen,
#               FigletText(str(game.score), "banner"),
#               score_top_padding, x=(screen.width - width) // 2 + 1,
#               colour=Screen.COLOUR_BLACK,
#               bg=Screen.COLOUR_BLACK,
#               speed=1),
#         Print(screen,
#               FigletText(str(game.score), "banner"),
#               score_top_padding,
#               colour=Screen.COLOUR_WHITE,
#               bg=Screen.COLOUR_WHITE,
#               speed=1),
#         stars_bg
#     ]
#
#     scenes.append(Scene(effects, duration=seconds_to_frame(4)))
#
#     screen.play(scenes, repeat=False, stop_on_resize=True)


def show_finish_screen(game):
    try:
        Screen.wrapper(animate, arguments=[game])
    except ResizeScreenError:
        pass
