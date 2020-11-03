#!/bin/env python3
from lib.sheet import Sheet

sheet_file = "demo"
sheet = Sheet(2, sheet_file, height=15, bpm=480)
sheet.start()
