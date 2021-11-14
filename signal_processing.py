from soapypower import __main__
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


def graph_data():
    datadf = pd.read_csv('raw_signal_data.csv', header=None)
    f0 = datadf.iloc[0, 2]
    f1 = datadf.iloc[-1, 3]
    df = datadf.iloc[0, 4]

    sig = np.array(datadf.iloc[:, 6:])
    sig = sig.flatten()
    freq = np.arange(f0, f1, df) / 1e6

    plt.plot(freq, sig)
    plt.xlim([freq[0], freq[-1]])
    plt.ylabel('PSD (dB)')
    plt.xlabel('Freq (GHz)')
    plt.show()


def pull_data():
    """
    edited __main__.py in C:\\Users\\jojok\\anaconda3\\Lib\\site-packages\\soapypower
    added a command line argument to main() in two places
    changed this line to include a command line argument args = parser.parse_args(command_line)
    """

    # set a gain value to keep data consistent
    command_line = ['-q', '-f', '1.2G', '-O', 'raw_signal_data.csv', '-g', '37.5', '-r', '6000000', '-k', '33.33']
    __main__.main(command_line)
    # if can't fix weird noise, take more samples and cut off the weird noise parts


pull_data()
graph_data()


'''import numpy

# List all connected SoapySDR devices
print(simplesoapy.detect_devices(as_string=True))

# Initialize SDR device
sdr = simplesoapy.SoapyDevice('driver=airspy')

# Set sample rate
sdr.sample_rate = 6e6

# Set center frequency
sdr.freq = 940e6

# Setup base buffer and start receiving samples. Base buffer size is determined
# by SoapySDR.Device.getStreamMTU(). If getStreamMTU() is not implemented by driver,
# SoapyDevice.default_buffer_size is used instead
sdr.start_stream()

# Create numpy array for received samples
samples = numpy.empty(len(sdr.buffer) * 100, numpy.complex64)

# Receive all samples
sdr.read_stream_into_buffer(samples)

# Stop receiving
sdr.stop_stream()'''
