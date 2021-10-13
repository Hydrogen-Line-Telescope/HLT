import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.stats import gaussian_kde
from mpl_toolkits.axes_grid1 import make_axes_locatable

freqdf = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\freq_data.csv')
magdf = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\mag_data.csv')
array = pd.DataFrame(freqdf).to_numpy()

mx = freqdf.to_numpy().max()
mn = freqdf.to_numpy().min()

cmap = colors.ListedColormap(['red', 'blue'])
bounds = [mn, 1420.405751, mx]
norm = colors.BoundaryNorm(bounds, cmap.N)
#cax = divider.append_axes('right', size='5%', pad=0.05)

fig, ax = plt.subplots()
canvas = fig.canvas

im = ax.imshow(freqdf, cmap=cmap, alpha=magdf, norm=norm)
#plt.colorbar(im)
plt.show()

fig1, ax1 = plt.subplots()
canvas1 = fig.canvas

im1 = ax1.imshow(freqdf, cmap=cmap, alpha=magdf, norm=norm, interpolation='catrom')
plt.show()

fig0, ax0 = plt.subplots()
canvas0 = fig.canvas

im0 = ax0.imshow(freqdf, cmap=cmap, alpha=magdf, norm=norm, interpolation='mitchell')
plt.show()

mx = magdf.to_numpy().max()
mn = magdf.to_numpy().min()

print(mx, mn)
