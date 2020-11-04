def handle_key(key):
    if key > -1:
        if key == ord("q"):
            raise BreakMainLoop


class BreakMainLoop(Exception):
    pass
