import subprocess
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from numpy.fft import rfft, rfftfreq, irfft


def filter_signal(signal, threshold=1e8):
    # rfft is the 1D discrete fourier transform for real input
    fourier = rfft(signal)
    print(fourier)
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

    # all data points in GHz
    freq = np.arange(start_freq, end_freq, freq_interval) / 1e9

    # find the peak magnitude and convert to a linear value
    peak_mag = np.amax(sig)
    peak_mag = np.exp(peak_mag/20)
    max_mag_index = np.where(sig == np.amax(sig))
    print("Peak Magnitude: ", peak_mag)

    # in GHz
    peak_freq = freq[int(max_mag_index[0])]
    # in MHz
    peak_freq = peak_freq * 1000
    print("Peak Frequency (MHz): ", peak_freq)

    freqdf = pd.DataFrame([peak_freq])
    magdf = pd.DataFrame([peak_mag])
    freqdf.to_csv('Peak Frequency.csv', index=False)
    magdf.to_csv('Peak Magnitude.csv', index=False)


# pull signal data using soapy_power
# -q, quiet the soapy_power module notifications
# -d, define driver used
# -f, define center frequency
# -O, output file name
# -g, gain, currently set to the default number
# -k, percentage of crop
# -n, number of spectra to average, default is 1600
'''command_line = subprocess.run(["soapy_power", "-q", "-d", "driver=rtlsdr", "-f", "1.2G", "-O", "signal_validation.csv",
                               "-g", "37.5", "-n", "12800"])'''

# ["soapy_power", "-q", "-d", "driver=rtlsdr", "-f", "1.2G", "-O", "signal_demo.csv", "-g", "37.5", "-n", "12800"]
# hydrogen line frequency, 1.420405751G
#get_freq_mag("TEST_ANTENNA_raw_signal_data.csv")
graph_data("TEST_ANTENNA_raw_signal_data.csv")

