#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

# collect the program file from the command line using sys.argv

if len(sys.argv) <= 1:
    print("Please provide a prgram file.")
elif len(sys.argv) > 1:
    file_name = sys.argv[1]
    print('File name in ls8.py', file_name)
    cpu = CPU()
    cpu.load(file_name)
    cpu.run()
