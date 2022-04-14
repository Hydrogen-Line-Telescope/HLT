import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import fake_mag_freq_data as foo
from functools import reduce


def hex_to_rgb(value):
    '''
    Converts hex to rgb colours
    value: string of 6 characters representing a hex colour.
    Returns: list length 3 of RGB values'''
    value = value.strip("#")  # removes hash symbol if present
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_dec(value):
    '''
    Converts rgb to decimal colours (i.e. divides each value by 256)
    value: list (length 3) of RGB values
    Returns: list (length 3) of decimal values'''
    return [v / 256 for v in value]


def plot_colortable(hex_list):
    cell_width = 150
    cell_height = 50
    swatch_width = 48
    margin = 12
    topmargin = 40

    rgb_list = [hex_to_rgb(value) for value in hex_list]
    dec_list = [rgb_to_dec(value) for value in rgb_list]
    names = [f'HEX: {col[0]}\nRGB: {col[1]}' for col in zip(hex_list, rgb_list, dec_list)]
    n = len(names)
    ncols = 3
    nrows = n // ncols + int(n % ncols > 0)

    width = cell_width * 8 + 2 * margin
    height = cell_height * nrows + margin + topmargin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(margin / width, margin / height,
                        (width - margin) / width, (height - topmargin) / height)
    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * (nrows - 0.5), -cell_height / 2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()

    for i, name in enumerate(names):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        swatch_end_x = cell_width * col + swatch_width
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(text_pos_x, y, name, fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')

        ax.hlines(y, swatch_start_x, swatch_end_x,
                  color=dec_list[i], linewidth=18)

    return fig


def get_continuous_cmap(hex_list, float_list=None):
    ''' creates and returns a color map that can be used in heat map figures.
        If float_list is not provided, colour map graduates linearly between each color in hex_list.
        If float_list is provided, each color in hex_list is mapped to the respective location in float_list.

        Parameters
        ----------
        hex_list: list of hex code strings
        float_list: list of floats between 0 and 1, same length as hex_list. Must start with 0 and end with 1.

        Returns
        ----------
        colour map'''
    rgb_list = [rgb_to_dec(hex_to_rgb(i)) for i in hex_list]
    if float_list:
        pass
    else:
        float_list = list(np.linspace(0, 1, len(rgb_list)))

    cdict = dict()
    for num, col in enumerate(['red', 'green', 'blue']):
        col_list = [[float_list[i], rgb_list[i][num], rgb_list[i][num]] for i in range(len(float_list))]
        cdict[col] = col_list
    cmp = colors.LinearSegmentedColormap('my_cmp', segmentdata=cdict, N=256)
    return cmp

# all of the above functions were taken from KerryHalupka on github to create a custom
# colormap for these heatmaps through matplotlib


def two_dim_sel(freqdf, magdf):
    # find max and min frequencies for red-blue shift bounds
    freq_max = freqdf.to_numpy().max()
    freq_min = freqdf.to_numpy().min()

    # creating the color bounds
    # red-shifted if frequency is less than 1420.4.. - moving away from telescope
    # blue-shifted if frequency is more than 1420.4.. - moving towards telescope
    # purple if frequency is near the middle - 1420.405 - range
    hex_list = ['#ff0000', '#800080', '#0000FF']
    cmap = get_continuous_cmap(hex_list)
    '''cmap = colors.ListedColormap(['red', 'blue'])'''
    bounds = [freq_min, 1420.4075, freq_max]
    norm = colors.TwoSlopeNorm(vmin=1419.40575, vcenter=1420.40575, vmax=1421.40575)

    # convert dataframe magdf to floats

    # creating the heatmap plot, interpolation set to 'catrom'
    fig, ax = plt.subplots()
    # norm=norm, alpha=magdf,
    #
    im = ax.imshow(freqdf, cmap=cmap, alpha=magdf, norm=norm, interpolation='catrom')
    #fig.colorbar(im)
    #fig.figure(facecolor='#A4A4A4')

    plt.axis('off')

    #plt.show()
    # save figure for overlay later
    #savefig('figname.png', facecolor=fig.get_facecolor(), transparent=True)
    # , facecolor='#A4A4A4', transparent=True
    plt.savefig('HeatMaps\\Heatmap.png', bbox_inches='tight', pad_inches=0)


def format_data_files(freq_file, mag_file, row):
    freqdf = pd.read_csv(freq_file)

    freqlist = freqdf['0'].tolist()

    # split list based off of row number
    split_freq = [freqlist[i:i + row] for i in range(0, len(freqlist), row)]

    # reverse every odd row to account for route path take by the motorized mount
    for i in range(len(split_freq)):
        if i % 2 != 0:
            split_freq[i].reverse()

    # put data into a DataFrame and write to a csv
    output_freq_df = pd.DataFrame(split_freq)
    output_freq_df_transposed = output_freq_df.transpose()
    output_freq_df_transposed.to_csv("Z:\\Signal Data\\format_freq_data.csv")

    # do the same for magdf
    magdf = pd.read_csv(mag_file)

    maglist = magdf['0'].tolist()

    # split list based off of row number
    split_mag = [maglist[i:i + row] for i in range(0, len(maglist), row)]

    # reverse every odd row to account for route path take by the motorized mount
    for i in range(len(split_mag)):
        if i % 2 != 0:
            split_mag[i].reverse()

    # put data into a DataFrame and write to a csv
    output_mag_df = pd.DataFrame(split_mag)
    output_mag_df_transposed = output_mag_df.transpose()
    output_mag_df_transposed.to_csv("Z:\\Signal Data\\format_mag_data.csv")


def two_dim_sweep(freqdf, magdf, num_scans):
    # data is in multiple columns, each scan is one column
    # number of columns is determined by the number of scans

    # get max and min frequencies from data
    freq_max = freqdf.to_numpy().max()
    freq_min = freqdf.to_numpy().min()

    # creating the color bounds
    # red-shifted if frequency is less than 1420.4.. - moving away from telescope
    # blue-shifted if frequency is more than 1420.4.. - moving towards telescope
    # cmap = colors.ListedColormap(['red', 'blue'])
    # bounds = [freq_min, 1420.405751, freq_max]
    #norm = colors.BoundaryNorm(bounds, cmap.N)

    hex_list = ['#ff0000', '#800080', '#0000FF']
    cmap = get_continuous_cmap(hex_list)
    norm = colors.TwoSlopeNorm(vmin=1419.40575, vcenter=1420.40575, vmax=1421.40575)

    # create a heatmap for each column of frequency and magnitude data
    # working from left to right
    for i in range(num_scans):
        freq_col = freqdf.columns.values.tolist()
        # print(freq_col)
        mag_col = magdf.columns.values.tolist()
        # print(mag_col)
        freq_list = freqdf[freq_col[i]].values.tolist()
        # print(freq_list)
        mag_list = magdf[mag_col[i]].values.tolist()
        # print(mag_list)
        magdf_scan = pd.DataFrame(mag_list)
        freqdf_scan = pd.DataFrame(freq_list)
        fig, ax = plt.subplots()
        im = ax.imshow(freqdf_scan, cmap=cmap, alpha=magdf_scan, norm=norm, interpolation='catrom')
        plt.axis('off')
        # save image for overlay later
        plt.savefig('Heatmaps\\Heatmap-' + str(i) + '.png', bbox_inches='tight', pad_inches=0)


def one_dim_sweep_rpa(freqdf, magdf, num_scans):
    # data is in one column, each scan is one pixel
    # number of pixels / length of column is determined by the number of scans
    freq_col = freqdf.columns.values.tolist()
    mag_col = magdf.columns.values.tolist()

    freq_list = freqdf[freq_col[0]].values.tolist()
    mag_list = magdf[mag_col[0]].values.tolist()

    freq_max = freqdf.to_numpy().max()
    freq_min = freqdf.to_numpy().min()

    '''if len(freq_list) == 1:
        bounds = [1400, 1420.405751, 1440]
    else:
        bounds = [freq_min, 1420.405751, freq_max]'''

    hex_list = ['#ff0000', '#800080', '#0000FF']
    cmap = get_continuous_cmap(hex_list)
    norm = colors.TwoSlopeNorm(vmin=1419.40575, vcenter=1420.40575, vmax=1421.40575)

    '''cmap = colors.ListedColormap(['red', 'blue'])
    # bounds = [freq_min, 1420.405751, freq_max]
    # bounds = [1400, 1420.405751, 1440]
    norm = colors.BoundaryNorm(bounds, cmap.N)'''

    # create a heatmap for each scanned pixel
    for i in range(num_scans):
        fig, ax = plt.subplots()
        im = ax.imshow([[freq_list[i]]], cmap=cmap, norm=norm, alpha=mag_list[i])
        plt.axis('off')
        plt.savefig('Heatmaps\\Heatmap-' + str(i) + '.png', bbox_inches='tight', pad_inches=0)


'''foo.two_dim_sweep_data(8, 6)
freqdf0 = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\freq_data_two_sweep.csv')
magdf0 = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\mag_data_two_sweep.csv')
two_dim_sel(freqdf0, magdf0)'''

'''foo.two_dim_sweep_data(6, 9)
freqdf1 = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\freq_data_two_sweep.csv')
magdf1 = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\mag_data_two_sweep.csv')
two_dim_sweep(freqdf1, magdf1, 6)'''

'''foo.two_dim_sweep_data(1, 10)
freqdf2 = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\freq_data_two_sweep.csv')
magdf2 = pd.read_csv('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\mag_data_two_sweep.csv')
one_dim_sweep_rpa(freqdf2, magdf2, 10)'''

# format_data_files('freq_data.csv', 'mag_data.csv', 6)
