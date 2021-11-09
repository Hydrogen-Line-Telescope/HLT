# Route Planner
import numpy as np


def normalize(max_r, c):
    c[0] = c[0] / max_r
    c[1] = c[1] / max_r

    return c


def inv_projection(max_r, c_cart):
    max_r = np.sqrt(2) * max_r

    c_sph = [0, 0]  # Phi, Theta
    c_sph_pp = [0, 0]  # Phi_x, Phi_y
    c_pol = [0, 0]  # R, Theta
    c_cart = normalize(max_r, c_cart)

    c_pol[0] = np.sqrt(c_cart[0] ** 2 + c_cart[1] ** 2)
    if c_cart[0] >= 0:
        c_pol[1] = np.arctan(c_cart[1] / c_cart[0]) * 180 / np.pi
    else:
        c_pol[1] = (np.arctan(c_cart[1] / c_cart[0]) * 180 / np.pi) + 180

    c_sph[0] = (2 * np.arcsin((np.sqrt(2) / 2) * c_pol[0]))
    c_sph[1] = c_pol[1] * np.pi / 180

    c_sph_pp[0] = (np.arctan((np.sin(c_sph[0]) * np.cos(c_sph[1])) / np.cos(c_sph[0]))) * (180 / np.pi)
    c_sph_pp[1] = (np.arctan((np.sin(c_sph[0]) * np.sin(c_sph[1])) / np.cos(c_sph[0]))) * (180 / np.pi)

    return c_sph_pp


def two_dim(max_r, c_l, c_r, hpbw):
    x_1 = c_l[0]
    y_1 = c_l[1]

    x_2 = c_r[0]
    y_2 = c_r[1]

    c_l_w = [x_1, y_1]
    c_r_w = [x_2, y_2]

    points_out = []

    c_s_l = inv_projection(max_r, c_l_w)
    c_s_r = inv_projection(max_r, c_r_w)

    phi_x_delta = c_s_r[0] - c_s_l[0]
    phi_y_delta = c_s_r[1] - c_s_l[1]

    num_points_x = int(np.ceil(phi_x_delta / hpbw))
    num_points_y = int(np.ceil(phi_y_delta / hpbw))

    for i in range(0, num_points_x + 1):
        for j in range(0, num_points_y + 1):
            phi_x = c_s_l[0] + (i * (phi_x_delta / num_points_x))
            phi_y = c_s_l[1] + (j * (phi_y_delta / num_points_y))

            next_point = np.around([phi_x, phi_y], decimals=0)
            next_point = next_point.tolist()

            points_out.append(next_point)

    return points_out


def two_terra(max_r, c, hpbw):
    points_out = []

    x = c[0] * c[0]

    y_1 = np.sqrt((max_r ** 2) - (x))
    y_2 = -1 * np.sqrt((max_r ** 2) - (x))

    c_t = [c[0], y_1]
    c_b = [c[0], y_2]

    c_s_t = inv_projection(max_r, c_t)
    c_s_b = inv_projection(max_r, c_b)

    phi_delta = c_s_t[1] - c_s_b[1]

    num_points = int(np.ceil(phi_delta / hpbw))

    for i in range(0, (num_points + 1)):
        phi_x = float(c_s_t[0])
        phi_y = float(c_s_b[1] + (i * (phi_delta / num_points)))

        next_point = np.around([phi_x, phi_y], decimals=0)
        next_point = next_point.tolist()

        points_out.append(next_point)

    return points_out


def one_terra(max_r, c):
    x_1 = c[0]
    y_1 = c[1]

    c_w = [x_1, y_1]

    c_s = inv_projection(max_r, c_w)

    c_s = np.around(c_s, decimals=0)
    c_s = c_s.tolist()

    return c_s


test_max_r = 500
test_c_ll = [-150, -75]
test_c_ur = [220, 450]
test_c = [-150, -75]
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
print(test_point_3)
