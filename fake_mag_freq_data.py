import pandas as pd
import numpy as np
import random


def two_dim_sel_data(height, width):
    # rectangular area
    # one scan
    rng_mag = np.random.default_rng(seed=70)
    mag = rng_mag.random((height, width))
    rng_freq = np.random.default_rng(seed=420)
    freq = rng_freq.random((height, width))*20+1410

    magdf = pd.DataFrame(mag)
    freqdf = pd.DataFrame(freq)

    magdf.to_csv('mag_data.csv', index=False)
    freqdf.to_csv('freq_data.csv', index=False)


def two_dim_sweep_data():
    x = 2


def one_dim_sweep_data(num_scans):
    # one pixel
    # multiple scans
    mag_list = []
    freq_list = []

    for i in range(num_scans):
        mag = random.random()
        freq =random.uniform(1410, 1430)
        mag_list.append(mag)
        freq_list.append(freq)

    magdf = pd.DataFrame(mag_list)
    freqdf = pd.DataFrame(freq_list)

    magdf.to_csv('mag_data.csv', index=False)
    freqdf.to_csv('freq_data.csv', index=False)


one_dim_sweep_data(5)
#two_dim_sel_data(6, 10)
