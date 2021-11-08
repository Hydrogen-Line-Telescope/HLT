#Route Planner
import numpy as np


def normalize(max_r, c):
    c[0] = c[0]/max_r
    c[1] = c[1]/max_r
    
    return c


def inv_projection(max_r, c_cart):
    c_sph = [0, 0] # Phi, Theta
    c_sph_pp = [0, 0] # Phi_x, Phi_y
    c_pol = [0, 0] # R, Theta
    c_cart = normalize(max_r, c_cart)
    
    c_pol[0] = np.sqrt(c_cart[0]**2 + c_cart[1]**2)
    if c_cart[0] >= 0:
        c_pol[1] = np.arctan(c_cart[1]/c_cart[0]) * 180/np.pi     
    else:
        c_pol[1] = (np.arctan(c_cart[1]/c_cart[0]) * 180/np.pi) + 180
        
    c_sph[0] = (2 * np.arcsin((np.sqrt(2)/2) * c_pol[0]))
    c_sph[1] = c_pol[1] * np.pi/180

    c_sph_pp[0] = (np.arctan((np.sin(c_sph[0]) * np.cos(c_sph[1])) / np.cos(c_sph[0]))) * (180/np.pi)
    c_sph_pp[1] = (np.arctan((np.sin(c_sph[0]) * np.sin(c_sph[1])) / np.cos(c_sph[0]))) * (180/np.pi)

    print("c_cart: ", c_cart)
    print("c_pol: ", c_pol)
    print("c_sph: ", c_sph)
    print("c_sph_pp: ", c_sph_pp)
    
    return c_sph_pp
    
    
def two_dim(max_r, c_l, c_r, hpbw):
    
    max_r = np.sqrt(2) * max_r
    points_out = []
    next_point = [0,0] #phi_x, phi_y
    
    c_s_l = inv_projection(max_r, c_l)
    c_s_r = inv_projection(max_r, c_r)

    phi_x_delta = c_s_r[0] - c_s_l[0]
    phi_y_delta = c_s_r[1] - c_s_l[1]

    num_points_x = np.ceil(phi_x_delta/hpbw)
    num_points_y = np.ceil(phi_y_delta/hpbw)
    
    num_points_x = int(num_points_x)
    num_points_y = int(num_points_y)
    
    print(num_points_x)
    print(num_points_y)
    print(c_s_l)
    print(c_s_r)
    
    for i in range(0, num_points_x + 1):
        for j in range(0, num_points_y + 1):
            
            phi_x = c_s_l[0] + (i * (phi_x_delta / num_points_x))
            phi_y = c_s_l[1] + (j * (phi_y_delta / num_points_y))
            
            next_point = [phi_x, phi_y]
            
            points_out.append(next_point)
            
    return points_out


test_max_r = 500
test_c_ll = [-150, -75]   
test_c_ur = [220, 450]
test_hpbw = 10
test_points = two_dim(test_max_r, test_c_ll, test_c_ur, test_hpbw)

print(test_points)