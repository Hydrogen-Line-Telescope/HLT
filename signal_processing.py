import subprocess
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from numpy.fft import rfft, rfftfreq, irfft
from csv import writer


def filter_signal(signal, threshold):
    # rfft is the 1D discrete fourier transform for real input
    fourier = rfft(signal)
    # rfftfreq is the discrete fourier transform sample for frequencies
    # d is one over the sample rate
    frequencies = rfftfreq(signal.size, d=1e-5)
    # apply the threshold value
    fourier[frequencies > threshold] = 0
    # irfft is the inverse of rfft
    return irfft(fourier)


def graph_data(file_name):
    """
    this function graphs the pulled signal data and is for testing purposes only
    """
    datadf = pd.read_csv(file_name, header=None)
    f0 = datadf.iloc[0, 2]
    f1 = datadf.iloc[-1, 3]
    df = datadf.iloc[0, 4]

    sig = np.array(datadf.iloc[:, 6:])
    sig = sig.flatten()

    linear_sig = []
    for i in sig:
        new_i = np.exp(i/20)
        linear_sig.append(new_i)

    freq = np.arange(f0, f1, df) / 1e9

    linear_sig = np.array(linear_sig)

    # trying out different thresholds
    for threshold in [1e3, 5e3, 1e4, 5e4]:
        filtered_sig = filter_signal(linear_sig, threshold)
        filtered_sig = filtered_sig[5:-5]
        freq = freq[5:-5]
        linear_sig = linear_sig[5:-5]
        # print(len(filtered_sig))
        # print(len(freq))
        plt.plot(freq, linear_sig, label='Raw')
        plt.plot(freq, filtered_sig, label='Filtered')
        # plt.xlim((freq[0], freq[-1]))
        plt.ylabel('Magnitude')
        plt.xlabel('Freq (GHz)')
        plt.legend()
        plt.title(f"FFT Denoising with threshold = {threshold :.0e}", size=15)
        plt.show()


def get_freq_mag(file_name):
    datadf = pd.read_csv(file_name, header=None)

    start_freq = datadf.iloc[0, 2]
    end_freq = datadf.iloc[-1, 3]
    freq_interval = datadf.iloc[0, 4]

    # list of signal magnitudes in dB
    sig = np.array(datadf.iloc[:, 6:])
    sig = sig.flatten()

    linear_sig = []
    for i in sig:
        new_i = np.exp(i / 20)
        linear_sig.append(new_i)

    linear_sig = np.array(linear_sig)

    filtered_sig = filter_signal(linear_sig, 5e3)

    # all data points in GHz
    freq = np.arange(start_freq, end_freq, freq_interval) / 1e9

    filtered_sig = filtered_sig[5:-5]
    freq = freq[5:-5]

    # find the peak magnitude and convert to a linear value
    peak_mag = np.amax(filtered_sig)
    max_mag_index = np.where(filtered_sig == np.amax(filtered_sig))
    print("Peak Magnitude: ", peak_mag)

    # in GHz
    peak_freq = freq[int(max_mag_index[0])]
    # in MHz
    peak_freq = peak_freq * 1000
    print("Peak Frequency (MHz): ", peak_freq)

    freqdf = [peak_freq]
    magdf = [peak_mag]
    print(freqdf)
    print(magdf)

    # append values to csv files for frequency and magnitude
    # 1 sweep & RPA are 1 columns
    # 2D sel & sweep are multiple columns
    # 2 sweep - num_scans = # col, route returns # row
    with open('Z:\\Signal Data\\freq_data.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(freqdf)
        f_object.close()

    with open('Z:\\Signal Data\\mag_data.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(magdf)
        f_object.close()


def write_blank_files():
    df = pd.DataFrame(list(" "))
    df.to_csv('Z:\\Signal Data\\freq_data.csv', index=False)
    df.to_csv('Z:\\Signal Data\\mag_data.csv', index=False)


def read_signal():
    # pull signal data using soapy_power
    # -q, quiet the soapy_power module notifications
    # -d, define driver used
    # -f, define center frequency
    # -O, output file name
    # -g, gain, currently set to the default number
    # -k, percentage of crop
    # -n, number of spectra to average, default is 1600
    command_line = subprocess.run(["soapy_power", "-q", "-d", "driver=rtlsdr", "-f", "1.2G", "-O",
                                   "raw_signal_data.csv", "-g", "37.5", "-n", "12800"])

    # ["soapy_power", "-q", "-d", "driver=rtlsdr", "-f", "1.2G", "-O", "signal_demo.csv", "-g", "37.5", "-n", "12800"]
    # hydrogen line frequency, 1.420405751G
    get_freq_mag('raw_signal_data.csv')


#get_freq_mag("TEST_ANTENNA_raw_signal_data.csv")
#graph_data("TEST_ANTENNA_raw_signal_data.csv")
'''write_blank_files()
get_freq_mag("TEST_ANTENNA_raw_signal_data.csv")
get_freq_mag("TEST_ANTENNA_raw_signal_data.csv")
get_freq_mag("TEST_ANTENNA_raw_signal_data.csv")
get_freq_mag("TEST_ANTENNA_raw_signal_data.csv")
get_freq_mag("TEST_ANTENNA_raw_signal_data.csv")
get_freq_mag("TEST_ANTENNA_raw_signal_data.csv")

print(pd.read_csv('freq_data.csv'))
print(pd.read_csv('mag_data.csv'))'''
