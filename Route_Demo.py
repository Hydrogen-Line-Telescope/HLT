# Route Planner
import numpy as np


def normalize(max_r, c):
    # normalizes the coordinates from pixel to equal area projection
    c[0] = c[0] / max_r
    c[1] = c[1] / max_r

    return c


def inv_projection(max_r, c_cart):
    # the image only includes 70 degrees so it needs to increase the max radius to the max radius of the equal area projection
    max_r = 1.515 * max_r

    # initializes values
    c_sph = [0, 0]  # Phi, Theta
    c_sph_pp = [0, 0]  # Phi_x, Phi_y
    c_pol = [0, 0]  # R, Theta
    c_cart = normalize(max_r, c_cart)

    # creates radius to be used in projection mapping
    c_pol[0] = np.sqrt(c_cart[0] ** 2 + c_cart[1] ** 2)

    # creates the theta value for projection mapping all of the ifs are to fix arctan
    if c_cart[0] > 0:
        c_pol[1] = np.arctan(c_cart[1] / c_cart[0])
    elif c_cart[0] == 0 and c_cart[1] > 0:
        c_pol[1] = 90
    elif c_cart[0] == 0 and c_cart[1] < 0:
        c_pol[1] = 270
    elif c_cart[0] == 0 and c_cart[1] == 0:
        c_pol[1] = 0
    else:
        c_pol[1] = (np.arctan(c_cart[1] / c_cart[0]) ) + np.pi

    # converts from equal area projection to spherical
    c_sph[0] = (2 * np.arcsin((np.sqrt(2) / 2) * c_pol[0]))
    c_sph[1] = c_pol[1]

    # converts from spherical to my coordinate system
    c_sph_pp[0] = (np.arctan((np.sin(c_sph[0]) * np.cos(c_sph[1])) / np.cos(c_sph[0]))) * (180 / np.pi)
    c_sph_pp[1] = (np.arctan((np.sin(c_sph[0]) * np.sin(c_sph[1])) / np.cos(c_sph[0]))) * (180 / np.pi)

    # returns the coordinate
    return c_sph_pp


def two_dim(max_r, c_l, c_r, hpbw):
    
    # initializes so that the used values don't mess with the passed in references
    x_1 = c_l[0]
    y_1 = c_l[1]

    x_2 = c_r[0]
    y_2 = c_r[1]

    c_l_w = [x_1, y_1]
    c_r_w = [x_2, y_2]

    # creates output array

    points_out = []

    # gets the two corner values
    c_s_l = inv_projection(max_r, c_l_w)
    c_s_r = inv_projection(max_r, c_r_w)

    # makes the delta between them to figure out the correct number of points
    phi_x_delta = c_s_r[0] - c_s_l[0]
    phi_y_delta = c_s_r[1] - c_s_l[1]

    # calculates the total number of points
    num_points_x = int(np.ceil(phi_x_delta / hpbw))
    num_points_y = int(np.ceil(phi_y_delta / hpbw))

    points_out_wo = [[0 for i in range(num_points_y+2)] for j in range(num_points_x+2)]

    # interpolates the new points to be used in the final image
    for i in range(0, num_points_x + 1):
        for j in range(0, num_points_y + 1):
            inbetween_x = x_1 + (i * ((x_2 - x_1) / num_points_x))
            inbetween_y = y_1 + (j * ((y_2 - y_1) / num_points_y))

            next_point = np.around([inbetween_x, inbetween_y], decimals=0)
            next_point = next_point.tolist()

            points_out_wo[i][j] = next_point

    for i in range(0, num_points_x + 1):
        for j in range(0, num_points_y + 1):
            if (i % 2) == 0:
                points_out.append(points_out_wo[i][num_points_y - j])
            else:
                points_out.append(points_out_wo[i][j])


    # projection maps them to get the correct list of points
    for i in range(0, len(points_out)):
        inbetween = inv_projection(max_r, points_out[i])

        next_point = np.around(inbetween, decimals=0)
        next_point = next_point.tolist()

        points_out[i] = next_point

    return points_out, num_points_y, num_points_x


def two_terra(max_r, c, hpbw):
    
    # pass values so global variables don't get changed
    x_in = c[0]
    x = c[0] * c[0]

    # calculates the top and bottom of the circle to further interpolate points
    y_1 = np.sqrt((max_r ** 2) - x)
    y_2 = -1 * np.sqrt((max_r ** 2) - x)

    # creates output list
    c_s_out = []

    # creates inbetween points
    for i in range(0, int(((y_1 - y_2)/34)) + 1):
        c_in = inv_projection(max_r, [x_in, int((y_1 - (i*34)))])
        c_in = np.around(c_in, decimals=0)
        c_s_out.append(c_in)

    return c_s_out, len(c_s_out)


def one_terra(max_r, c):

    # just one inverse projection
    x_1 = c[0]
    y_1 = c[1]

    c_w = [x_1, y_1]

    c_s = inv_projection(max_r, c_w)

    c_s = np.around(c_s, decimals=0)
    c_s = c_s.tolist()

    return c_s


'''test_max_r = 500
test_c_ll = [-150, -75]
test_c_ur = [220, 450]
test_c = [0, 0]
test_hpbw = 10

test_points_1 = two_dim(test_max_r, test_c, test_c_ur, test_hpbw)

test_points_2 = two_terra(test_max_r, test_c_ll, test_hpbw)

test_point_3 = one_terra(test_max_r, test_c)

print("2-D Area Scan")
print(test_points_1)
print()
print("2-D Terrestrial Sweep")
print(test_points_2)
print()
print("1-D Terrestrial Sweep & Repeated Point Analysis")
print(test_point_3)'''
