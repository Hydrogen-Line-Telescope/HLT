from soapypower import __main__
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


def graph_data():
    datadf = pd.read_csv('raw_signal_data_set.csv', header=None)
    f0 = datadf.iloc[0, 2]
    f1 = datadf.iloc[-1, 3]
    df = datadf.iloc[0, 4]

    sig = np.array(datadf.iloc[:, 6:])
    sig = sig.flatten()

    linear_sig = []
    for i in sig:
        new_i = np.exp(i/20)
        linear_sig.append(new_i)
    print(linear_sig)

    freq = np.arange(f0, f1, df) / 1e9

    plt.plot(freq, linear_sig)
    plt.xlim([freq[0], freq[-1]])
    plt.ylabel('PSD (dB)')
    plt.xlabel('Freq (GHz)')
    plt.show()


def get_freq_mag():
    datadf = pd.read_csv('raw_signal_data.csv', header=None)

    start_freq = datadf.iloc[0, 2]
    end_freq = datadf.iloc[-1, 3]
    freq_interval = datadf.iloc[0, 4]

    # list of signal magnitudes in dB
    sig = np.array(datadf.iloc[:, 6:])
    sig = sig.flatten()

    # all data points in GHz
    freq = np.arange(start_freq, end_freq, freq_interval) / 1e9

    # find the peak magnitude and convert to a linear value
    peak_mag = np.amax(sig)
    peak_mag = np.exp(peak_mag/20)
    max_mag_index = np.where(sig == np.amax(sig))
    print("Peak Magnitude: ", peak_mag)

    # in GHz
    peak_freq = freq[int(max_mag_index[0])]
    print("Peak Frequency (GHz): ", peak_freq)

    freqdf = pd.DataFrame([peak_freq])
    magdf = pd.DataFrame([peak_mag])
    freqdf.to_csv('Peak Frequency.csv', index=False)
    magdf.to_csv('Peak Magnitude.csv', index=False)


def pull_data():
    """
    edited __main__.py in C:\\Users\\jojok\\anaconda3\\Lib\\site-packages\\soapypower
    added a command line argument to main() in two places
    changed this line to include a command line argument args = parser.parse_args(command_line)
    """

    # set a gain value to keep data consistent
    command_line = ['-q', '-f', '1.42G', '-O', 'raw_signal_data.csv', '-g', '37.5', '-r', '6000000', '-k', '33.33',
                    '-n', '12800']
    __main__.main(command_line)


pull_data()
get_freq_mag()
graph_data()
