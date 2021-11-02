import pandas as pd
import numpy as np


def calculate_coordinates(x, y):

    max_radius = 150
    r = np.sqrt(x**2 + y**2)/max_radius
    theta = np.arctan(y/x) * (180/np.pi)
    phi = (2*np.arcsin((np.sqrt(2)/2)*r)) * (180/np.pi)

    return theta, phi


def read_from_gui(mode, guidf):
    # mode - which mode the user selected, int
    #   -> 1, 2-DSel
    #   -> 2, 2-DTS
    #   -> 3, 1-DTS
    #   -> 4, RPA

    # pixel_s - pixel coordinate(s) from the sky map photo, list

    if mode == 1:
        guidf.loc[3] = [guidf.iloc[0, 0], guidf.iloc[1, 1]]
        guidf.loc[4] = [guidf.iloc[1, 0], guidf.iloc[0, 1]]
        cornerdf = pd.DataFrame()

        calculate_coordinates(guidf.iloc[0, 0], guidf.iloc[0, 1])



        print(guidf.loc[3])
        print(guidf)
    elif mode == 2:
        # hard code in starting line end points
        endpoints = [[150, 300], [150, 0]]
        guidf = pd.DataFrame(endpoints)
        print(guidf)
    elif mode == 3:
        print(guidf)
    elif mode == 4:

        print(guidf)


def earth_rotation():
    # figure out how much time between scans
    # figure out which direction the earth is rotating
    # assume college station, tx location

    # earth is rotating from west towards the east (90 degrees from our location) at 15 degrees an hour
    # in order to scan the sky at 10 degree increments
    #   - scan every 2/3 hour or 40 min

    y = 3


#calculate_coordinates(50, 150)

gui_list = [[50, 100], [275, 150]]
guidf = pd.DataFrame(gui_list)

read_from_gui(1, guidf)
