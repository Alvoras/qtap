from lib.exceptions import BreakMainLoop, QuitGame


def handle_key(key):
    if key > -1:
        if key == ord("q"):
            raise QuitGame
        if key == ord("m"):
            raise BreakMainLoop
