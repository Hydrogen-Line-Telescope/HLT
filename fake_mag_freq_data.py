import pandas as pd
import seaborn as sns
import numpy as np

mag = []
freq = []

rng_mag = np.random.default_rng(seed=69)
mag = rng_mag.random((9, 36))
rng_freq = np.random.default_rng(seed=420)
freq = rng_freq.random((9, 36))*20+1410

magdf = pd.DataFrame(mag)
freqdf = pd.DataFrame(freq)

magdf.to_csv('mag_data.csv', index=False)
freqdf.to_csv('freq_data.csv', index=False)
