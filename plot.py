#!/bin/env python3
# ----------------
# Script:     plot.py
# Programmer: Mavridis Philippe
# Date:       2021/11/08

import numpy             as np
import pandas            as pd
import datetime          as dt
import matplotlib.pyplot as pl
from   sys import argv

MODES = {
    'full':     "Display data for all years",
    'crisis':   "Data around the economic crisis period"
}
MODE = list(MODES.keys())[0] # pick default mode

# "Constants"
YEAR_RANGE = {
    'full':     None,
    'crisis':   (2006, 2015)
}

def trim_label(text):
    return text.replace("_", " ")

if __name__ == "__main__":
    # Parse command-line arguments
    for a in argv:
        if a in ("--help", "-h"):
            print("usage: ./plot.py [--help|-h] <mode>")
            print("")
            print("--help   Prints this message.")
            print("")
            print("Available modes:")
            for mode in MODES:
                print("  {}   {}".format(mode, MODES[mode]))
            exit(0)

        elif a in MODES:
            MODE = a

    # Initialize arrays and parse data
    date, value = [], []
    frame       = pd.read_excel("data.xls")

    # For our convenience
    COL_YEAR = frame.columns[0]
    COL_QUAR = frame.columns[1]
    COL_VAL  = frame.columns[2]

    # Keep only data we need
    if( YEAR_RANGE[MODE] is not None ):
        frame = frame[ frame[COL_YEAR] >= YEAR_RANGE[MODE][0] ]
        frame = frame[ frame[COL_YEAR] <= YEAR_RANGE[MODE][1] ]
    print(frame)
    # Fetch values
    for i in range(0, len(frame)):
        date.append( dt.datetime(
            frame[COL_YEAR][i],
            frame[COL_QUAR][i] * 3,
            1
        ) )
        value.append( frame[COL_VAL][i] )

    # Convert to NumPy arrays
    date, value = np.array(date), np.array(value)

    # Plot
    pl.plot(date, value)

    # Axis titles
    pl.xlabel( trim_label("{}/{}".format(COL_YEAR, COL_QUAR)) )
    pl.ylabel( trim_label(COL_VAL) )

    # Display
    pl.show()
