#!/usr/bin/env python3

import sys
from compost.options import OptionsFile
from compost.pipeline import Pipeline


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Only call compost,py with one additional argument!")
    option = OptionsFile(sys.argv[1])
    pl = Pipeline()
    pl.execute_options(option)