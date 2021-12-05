import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import fake_mag_freq_data as foo


def two_dim_sel(freqdf, magdf):
    # find max and min frequencies for red-blue shift bounds
    freq_max = freqdf.to_numpy().max()
    freq_min = freqdf.to_numpy().min()

    # creating the color bounds
    # red-shifted if frequency is less than 1420.4.. - moving away from telescope
    # blue-shifted if frequency is more than 1420.4.. - moving towards telescope
    cmap = colors.ListedColormap(['red', 'blue'])
    bounds = [freq_min, 1420.405751, freq_max]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # creating the heatmap plot, interpolation set to 'catrom'
    fig, ax = plt.subplots()
    im = ax.imshow(freqdf, cmap=cmap, alpha=magdf, norm=norm, interpolation='catrom')
    plt.axis('off')

    # save figure for overlay later
    plt.savefig('HeatMaps\\2-DSel.png', bbox_inches='tight', pad_inches=0)


def two_dim_sweep(freqdf, magdf, num_scans):
    # data is in multiple columns, each scan is one column
    # number of columns is determined by the number of scans

    # get max and min frequencies from data
    freq_max = freqdf.to_numpy().max()
    freq_min = freqdf.to_numpy().min()

    # creating the color bounds
    # red-shifted if frequency is less than 1420.4.. - moving away from telescope
    # blue-shifted if frequency is more than 1420.4.. - moving towards telescope
    cmap = colors.ListedColormap(['red', 'blue'])
    bounds = [freq_min, 1420.405751, freq_max]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # create a heatmap for each column of frequency and magnitude data
    for i in range(num_scans):
        freq_col = freqdf.columns.values.tolist()
        mag_col = magdf.columns.values.tolist()
        freq_list = freqdf[freq_col[i]].values.tolist()
        mag_list = magdf[mag_col[i]].values.tolist()
        magdf_scan = pd.DataFrame(mag_list)
        freqdf_scan = pd.DataFrame(freq_list)
        fig, ax = plt.subplots()
        im = ax.imshow(freqdf_scan, cmap=cmap, norm=norm, alpha=magdf_scan, interpolation='catrom')
        plt.axis('off')
        # save image for overlay later
        plt.savefig('Heatmaps\\2-DTS_' + str(i) + '.png', bbox_inches='tight', pad_inches=0)


def one_dim_sweep_rpa(freqdf, magdf, num_scans):
    # data is in one column, each scan is one pixel
    # number of pixels / length of column is determined by the number of scans
    freq_col = freqdf.columns.values.tolist()
    mag_col = magdf.columns.values.tolist()

    freq_list = freqdf[freq_col[0]].values.tolist()
    mag_list = magdf[mag_col[0]].values.tolist()

    freq_max = freqdf.to_numpy().max()
    freq_min = freqdf.to_numpy().min()

    if len(freq_list) == 1:
        bounds = [1400, 1420.405751, 1440]
    else:
        bounds = [freq_min, 1420.405751, freq_max]

    cmap = colors.ListedColormap(['red', 'blue'])
    # bounds = [freq_min, 1420.405751, freq_max]
    # bounds = [1400, 1420.405751, 1440]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # create a heatmap for each scanned pixel
    for i in range(num_scans):
        fig, ax = plt.subplots()
        im = ax.imshow([[freq_list[i]]], cmap=cmap, norm=norm, alpha=mag_list[i])
        plt.axis('off')
        plt.savefig('Heatmaps\\1-DTS_RPA_' + str(i) + '.png', bbox_inches='tight', pad_inches=0)


foo.two_dim_sel_data(6, 8)
freqdf0 = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\freq_data_two_sel.csv')
magdf0 = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\mag_data_two_sel.csv')
two_dim_sel(freqdf0, magdf0)

foo.two_dim_sweep_data(5, 8)
freqdf1 = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\freq_data_two_sweep.csv')
magdf1 = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\mag_data_two_sweep.csv')
two_dim_sweep(freqdf1, magdf1, 5)

foo.one_dim_sweep_rpa_data(1)
freqdf2 = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\freq_data_one_sweep.csv')
magdf2 = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\mag_data_one_sweep.csv')
'''freqdf2 = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Peak Frequency.csv')
magdf2 = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Peak Magnitude.csv')'''
one_dim_sweep_rpa(freqdf2, magdf2, 1)
