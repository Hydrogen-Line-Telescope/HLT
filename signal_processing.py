import simplesoapy
import numpy

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
sdr.stop_stream()


'''from rtlsdr import RtlSdr

sdr = RtlSdr(1)


#print(sdr)

# configure device
sdr.sample_rate = 2.048e6  # Hz
sdr.center_freq = 2.4115e9     # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

print(sdr.read_samples(512))
'''

'''import simplesoapy
import numpy

# List all connected SoapySDR devices
print(simplesoapy.detect_devices(as_string=True))

# Initialize SDR device
sdr = simplesoapy.SoapyDevice('driver=rtlsdr')

# Set sample rate
sdr.sample_rate = 2.56e6

# Set center frequency
sdr.freq = 88e6

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




'''from rtlsdr import RtlSdr

sdr = RtlSdr(1)

print(sdr)'''

'''# configure device
sdr.sample_rate = 2.048e6  # Hz
sdr.center_freq = 2.4115e9     # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

print(sdr.read_samples(512))'''

'''from rtlsdr import RtlSdr

# Get a list of detected device serial numbers (str)
serial_numbers = RtlSdr.get_device_serial_addresses()

print(serial_numbers)'''

'''# Find the device index for a given serial number
device_index = RtlSdr.get_device_index_by_serial('00000001')

sdr = RtlSdr(device_index)

# Or pass the serial number directly:
sdr = RtlSdr(serial_number='00000001')'''