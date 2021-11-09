#!/bin/env python3
#-*- coding: utf-8 -*-
# ----------------
# Script:     plot.py
# Programmer: Mavridis Philippe
# Date:       2021/11/08

import numpy             as np
import pandas            as pd
import datetime          as dt
import matplotlib.pyplot as pl
from   sys      import argv
from   os.path  import isfile

# "Constants"
MODES = {
    'full':     "Δεδομένα για όλα τα διαθέσιμα χρόνια",
    'crisis':   "Δεδομένα σχετικά με την περίοδο της οικονομικής κρίσης"
}
MODE = list(MODES.keys())[0] # pick default mode
PLOT_SAVE = None
PLOT_DISPLAY = None

YEAR_RANGE = {
    'full':     None,
    'crisis':   (2006, 2015)
}

DATA_URL = "https://www.bankofgreece.gr/OpenDataSetFilesALL/DOAM/New_Index_of_Apartment_Prices_by_Geographical_Area_el_2021-09-09.xls"

# Functions
def trim_label(text):
    return text.replace("_", " ")

if __name__ == "__main__":
    # Parse command-line arguments
    for a in argv[1:]:
        if a in ("--help", "-h"):
            print("usage: ./plot.py [--help|-h] <λειτουργία>")
            print("")
            print("--help      (-h)   Αυτό το μήνυμα.")
            print("--save      (-s)   Αποθήκευση γραφήματος ως εικόνας PNG.")
            print("--display   (-d)   Απεικόνιση γραφήματος σε παράθυρο (προεπιλογή).")
            print("")
            print("Διαθέσιμες λειτουργίες:")
            for mode in MODES:
                print("  {}{}".format(mode.ljust(10, ' '), MODES[mode]))
            exit(0)

        elif a in ("--save", "-s"):
            PLOT_SAVE    = True

        elif a in ("--display", "-d"):
            PLOT_DISPLAY = True

        elif a in MODES:
            MODE = a

        else:
            print("Σφάλμα: άγνωστη παράμετρος '{}'".format(a))
            print("Εκτελέστε την εντολή './plot.py --help' για να δείτε το μήνυμα βοήθειας.")
            exit(1)

    # Check whether we have the data. If not, silently download it.
    if not isfile("data.xls"):
        try:
            from urllib import request as r
            r.urlretrieve(DATA_URL, "data.xls")
        except Exception as e:
            print("Αδυναμία λήψης δεδομένων: {}".format(e.msg))
            exit(2)

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

    # Save
    if PLOT_SAVE:
        datestr = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        pl.savefig(
            "plot-{}-{}.png".format(MODE, datestr),
            transparent = True
        )

    # Display
    if PLOT_DISPLAY or (PLOT_DISPLAY is None and PLOT_SAVE is None):
        pl.show()
