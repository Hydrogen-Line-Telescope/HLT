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
    plt.savefig('TestFolder\\2-DSel.png', bbox_inches='tight', pad_inches=0)


#def two_dim_sweep(freqdf, magdf):


def one_dim_sweep(freqdf, magdf, num_scans):

    freq_col = freqdf.columns.values.tolist()
    mag_col = magdf.columns.values.tolist()

    freq_list = freqdf[freq_col[0]].values.tolist()
    mag_list = magdf[mag_col[0]].values.tolist()

    freq_max = freqdf.to_numpy().max()
    freq_min = freqdf.to_numpy().min()

    cmap = colors.ListedColormap(['red', 'blue'])
    bounds = [freq_min, 1420.405751, freq_max]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    for i in range(num_scans):
        print(freq_list[i])
        fig, ax = plt.subplots()
        im = ax.imshow([[freq_list[i]]], cmap=cmap, norm=norm, alpha=mag_list[i])
        plt.axis('off')
        plt.savefig('TestFolder\\2-DTS_' + str(i) + '.png', bbox_inches='tight', pad_inches=0)

    print(freqdf)
    print(freq_list)
    print(mag_list)
    print(mag_list[1])


freqdf = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\freq_data.csv')
magdf = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\mag_data.csv')

#two_dim_sel(freqdf, magdf)
one_dim_sweep(freqdf, magdf, 5)
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
im = ax.imshow([[1.5]])
plt.show()'''