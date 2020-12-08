#!/usr/bin/env python3
import argparse
import qrng


def generate(qbit, out, tick, bpm):
    tracks = []
    track_qty = pow(2, qbit)
    symbols = ["{0:b}".format(n).zfill(qbit) for n in range(track_qty)]
    tick_delay = round(tick * (bpm/60))

    qrng.set_provider_as_IBMQ('')
    qrng.set_backend()

    for i in range(1, track_len):
        line = ["-"*qbit]*len(symbols)

        if i % tick_delay == 0:  # Add a symbol every $tick_delay
            rng = qrng.get_random_int(0, len(line) - 1)

            line[rng] = symbols[rng]

        tracks.append(" ".join(line))

    with open(f"{out}.qtap{str(qbit)}", "w") as f:
        f.write("\n".join(tracks))


parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bpm", required=True, type=int, dest="bpm", help="BPM")
parser.add_argument("-d", "--duration", required=True, type=int, dest="duration", help="Duration (seconds)")
parser.add_argument("-q", "--qbit", default=2, type=int, dest="qbit", choices=[2, 3], help="Qbit quantity")
parser.add_argument("-t", "--tick", default=5, type=float, dest="tick", help="Seconds between each symbol")
parser.add_argument("-f", "--full", dest="full", action="store_true", help="Generate easy and hard sheets for 2 and 3 qbits")
parser.add_argument("-o", "--out", default="out", dest="out", help="Output file (without extension)")
args = parser.parse_args()

track_len = round((args.bpm/60) * args.duration)

if args.full:
    tick_presets = {
        "easy": {
            "2": 2,
            "3": 4
        },
        "hard": {
            "2": 1,
            "3": 2
        }
    }

    for qbit in [2, 3]:
        for mode in ["easy", "hard"]:
            generate(qbit, mode, tick_presets[mode][str(qbit)], args.bpm)
else:
    generate(args.qbit, args.out, args.tick, args.bpm)
