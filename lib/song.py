import os

import yaml
from PIL import Image

from lib import asciify
from lib.exceptions import MissingSongParam, UnsupportedDifficultyMode, MissingSongSheet


class Song:
    def __init__(self, meta_file, mode, songs_root, width, height):
        self.cover = None
        self.mode = mode
        with open(meta_file) as f:
            meta = yaml.load(f, Loader=yaml.FullLoader)
            self.author = meta["author"]
            self.name = meta["name"]
            self.music_file = os.path.join(songs_root, meta["music_file"])
            if "sheets" in meta:
                try:
                    self.sheet_file = meta["sheets"][self.mode]
                except KeyError:
                    raise UnsupportedDifficultyMode

                if self.sheet_file == "N/A":
                    raise UnsupportedDifficultyMode
            else:
                raise MissingSongParam

            self.sheet_file = os.path.join(songs_root, self.sheet_file)
            if not os.path.exists(self.sheet_file):
                raise MissingSongSheet(f"Missing sheet path ({self.sheet_file})")

            self.bpm = meta["bpm"]
            max_len = max(width, height)
            self.cover_width = max_len + 1
            # raise Exception(self.cover_width)

            if meta.get("cover"):
                self.cover_path = os.path.join(songs_root, meta.get("cover"))
                # self.cover_width = ((width // 3) // 2) + 1

                if self.cover_path:
                    try:
                        split_cover = asciify.to_ascii(self.cover_path, new_width=self.cover_width).split()
                        self.cover = [" ".join(c for c in line) for line in split_cover]
                    except FileNotFoundError:
                        # print("Unable to find image in", self.cover_path)
                        pass
            else:
                lines = []
                for _ in range(self.cover_width):
                    line = " ".join(c for c in [line for line in ["."]*self.cover_width])
                    lines.append(line)
                self.cover = lines
