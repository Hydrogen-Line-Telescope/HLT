import pandas as pd
import numpy as np


def calculate_coordinates(x, y, max_radius):

    r = np.sqrt(x**2 + y**2)/max_radius
    if x < 0:
        theta = np.arctan(y/x) * (180/np.pi) + 180
    # (x >= 0)
    else:
        theta = np.arctan(y / x) * (180 / np.pi)
    phi = (2*np.arcsin((np.sqrt(2)/2)*r)) * (180/np.pi)

    return theta, phi


def read_from_gui(mode, xydf):
    # mode - which mode the user selected, int
    #   -> 1, 2-DSel
    #   -> 2, 2-DTS
    #   -> 3, 1-DTS
    #   -> 4, RPA

    # pixel_s - pixel coordinate(s) from the sky map photo, list

    max_radius = 300

    if mode == 1:
        xydf.loc[3] = [xydf.iloc[0, 0], xydf.iloc[1, 1]]
        xydf.loc[4] = [xydf.iloc[1, 0], xydf.iloc[0, 1]]
        sphericaldf = pd.DataFrame()

        for i in range(4):
            theta, phi = calculate_coordinates(xydf.iloc[i, 0], xydf.iloc[i, 1], max_radius)
            tempdf = pd.DataFrame([[theta, phi]])
            sphericaldf = pd.concat([sphericaldf, tempdf])

        sphericaldf.rename(columns={0: 'θ', 1: 'ϕ'}, inplace=True)
        print(xydf)
        print(sphericaldf)
    elif mode == 2:
        # hard code in starting line end points
        x = guidf.iloc[0, 0]
        norm_x = x/max_radius
        y = np.sqrt(1 - norm_x**2)
        xydf = pd.DataFrame([[norm_x, y], [norm_x, -y]])
        xydf.rename(columns={0: 'x', 1: 'y'}, inplace=True)
        print(xydf)
        two_dim_terr_df = pd.DataFrame()
        for i in range(2):
            theta, phi = calculate_coordinates(xydf.iloc[i, 0], xydf.iloc[i, 1], max_radius)
            tempdf = pd.DataFrame([[theta, phi]])
            two_dim_terr_df = pd.concat([two_dim_terr_df, tempdf])
        two_dim_terr_df.rename(columns={0: 'θ', 1: 'ϕ'}, inplace=True)
        print(two_dim_terr_df)

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

# mode 1
'''gui_list = [[100, 200], [-200, -100]]
guidf = pd.DataFrame(gui_list)
read_from_gui(1, guidf)'''

# mode 2
gui_point = [[-50, 75]]
guidf = pd.DataFrame(gui_point)
read_from_gui(2, guidf)
