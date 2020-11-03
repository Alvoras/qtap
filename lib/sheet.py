import threading


class Sheet:
    def __init__(self, qbit_qty, height=20):
        self.tracks = []
        self.cursor = 0
        self.height = height

        for n in range(pow(qbit_qty, 2)):
            self.tracks.append("{0:b}".format(n).zfill(qbit_qty))

    def start(self):
        thread = threading.Thread(target=self.draw)
        thread.start()

    def draw(self):
        lines = []
        for line in range(self.height):
            lines.append(f" {line + self.cursor:03}   ")
            for track in self.tracks:
                lines[line] += f"{track} "

            lines[line] += " "

        print("\n".join(lines))

