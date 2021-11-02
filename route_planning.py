import pandas as pd
import numpy as np


def calculate_coordinates(x, y):

    max_radius = 300
    r = np.sqrt(x**2 + y**2)/max_radius
    theta = np.arctan(y/x) * (180/np.pi)
    phi = 90 - (2*np.arcsin((np.sqrt(2)/2)*r)) * (180/np.pi)

    print(r)
    print(theta, phi)

    return theta, phi


def read_from_gui(mode, xydf):
    # mode - which mode the user selected, int
    #   -> 1, 2-DSel
    #   -> 2, 2-DTS
    #   -> 3, 1-DTS
    #   -> 4, RPA

    # pixel_s - pixel coordinate(s) from the sky map photo, list

    if mode == 1:
        xydf.loc[3] = [xydf.iloc[0, 0], xydf.iloc[1, 1]]
        xydf.loc[4] = [xydf.iloc[1, 0], xydf.iloc[0, 1]]
        sphericaldf = pd.DataFrame()

        for i in range(4):
            theta, phi = calculate_coordinates(xydf.iloc[i, 0], xydf.iloc[i, 1])
            tempdf = pd.DataFrame([[theta, phi]])
            sphericaldf = pd.concat([sphericaldf, tempdf])

        sphericaldf.rename(columns={0: 'theta', 1: 'phi'})
        print(xydf)
        print(sphericaldf)
    elif mode == 2:
        # hard code in starting line end points
        endpoints = [[150, 300], [150, 0]]
        xydf = pd.DataFrame(endpoints)
        print(xydf)
    elif mode == 3:
        print(xydf)
    elif mode == 4:
        print(xydf)


def earth_rotation():
    # figure out how much time between scans
    # figure out which direction the earth is rotating
    # assume college station, tx location

    # earth is rotating from west towards the east (90 degrees from our location) at 15 degrees an hour
    # in order to scan the sky at 10 degree increments
    #   - scan every 2/3 hour or 40 min

    y = 3


#calculate_coordinates(50, 150)

gui_list = [[100, 200], [-200, -100]]
guidf = pd.DataFrame(gui_list)

read_from_gui(1, guidf)
