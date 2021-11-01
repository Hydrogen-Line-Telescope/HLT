from soapypower import __main__
from argparse import Namespace
import numpy as np
from matplotlib import pyplot as plt


def graph_data():
    with open('idk.csv', 'r') as csvfile:
        data_str = csvfile.read()  # Read the data
    data = data_str.split(',')  # Use comma as the delimiter

    timestamp = data[0] + data[1]  # Timestamp as YYYY-MM-DD hhh:mmm:ss
    f0 = float(data[2])  # Start Frequency
    f1 = float(data[3])  # Stop Frequency
    df = float(data[4])  # Frequency Spacing
    sig = np.array(data[6:], dtype=float)  # Signal data
    freq = np.arange(f0, f1, df) / 1e9  # Frequency Array

    # Plot the data
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

    command_line = ['-f', '1.2G', '-O', 'idk.csv', '-a']
    __main__.main(command_line)


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
