#!/usr/bin/env python3
import argparse
from random import randint

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bpm", required=True, type=int, dest="bpm", help="BPM")
parser.add_argument("-d", "--duration", required=True, type=int, dest="duration", help="Duration (seconds)")
parser.add_argument("-q", "--qbit", default=2, type=int, dest="qbit", choices=[2, 3], help="Qbit quantity")
parser.add_argument("-t", "--tick", default=5, type=int, dest="tick", help="Seconds between each symbol")
args = parser.parse_args()

tracks = []
track_len = round((args.bpm/60) * args.duration)

track_qty = pow(2, args.qbit)
symbols = ["{0:b}".format(n).zfill(args.qbit) for n in range(track_qty)]
tick_delay = round(args.tick * (args.bpm/60))

for i in range(1, track_len):
    line = ["-"*args.qbit]*len(symbols)

    if i % tick_delay == 0:  # Add a symbol every $tick_delay
        rng = randint(0, len(line) - 1)
        line[rng] = symbols[rng]

    tracks.append(" ".join(line))

with open("out", "w") as f:
    f.write("\n".join(tracks))
