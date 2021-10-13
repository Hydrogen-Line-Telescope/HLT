import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors


def two_dim_sel(freqdf, magdf):
    # find max and min frequencies for red-blue shift bounds
    freq_max = freqdf.to_numpy().max()
    freq_min = freqdf.to_numpy().min()

    cmap = colors.ListedColormap(['blue', 'red'])
    bounds = [freq_min, 1420.405751, freq_max]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()

    im = ax.imshow(freqdf, cmap=cmap, alpha=magdf, norm=norm, interpolation='catrom')
    plt.axis('off')
    plt.savefig('2-DSel.png', bbox_inches='tight', pad_inches=0)


#def two_dim_sweep(freqdf, magdf):


def one_dim_sweep(freqdf, magdf, num_scans):
    x = 2


freqdf = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\freq_data.csv')
magdf = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\mag_data.csv')

two_dim_sel(freqdf, magdf)

'''
array = pd.DataFrame(freqdf).to_numpy()

mx = freqdf.to_numpy().max()
mn = freqdf.to_numpy().min()

cmap = colors.ListedColormap(['blue', 'red'])
bounds = [mn, 1420.405751, mx]
norm = colors.BoundaryNorm(bounds, cmap.N)
#cax = divider.append_axes('right', size='5%', pad=0.05)

fig, ax = plt.subplots()
canvas = fig.canvas

im = ax.imshow(freqdf, cmap=cmap, alpha=magdf)#, alpha=magdf, norm=norm)
#plt.colorbar(im)
plt.show()
'''





'''
fig1, ax1 = plt.subplots()
canvas1 = fig.canvas

im1 = ax1.imshow(freqdf, cmap=cmap, alpha=magdf, norm=norm, interpolation='catrom')
plt.show()

fig0, ax0 = plt.subplots()
canvas0 = fig.canvas

im0 = ax0.imshow(freqdf, cmap=cmap, alpha=magdf, norm=norm, interpolation='mitchell')
plt.show()
'''
'''
mx = magdf.to_numpy().max()
mn = magdf.to_numpy().min()

#print(mx, mn)
fig, ax = plt.subplots()
im = ax.imshow([[1]])
plt.show()'''