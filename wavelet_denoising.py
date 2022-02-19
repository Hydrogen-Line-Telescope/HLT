import pywt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from numpy.fft import rfft, rfftfreq, irfft


def madev(d, axis=None):
    """ Mean absolute deviation of a signal """
    return np.mean(np.absolute(d - np.mean(d, axis)), axis)


def wavelet_denoising(x, wavelet='db4', level=1):
    coeff = pywt.wavedec(x, wavelet, mode="per")
    sigma = (1/0.6745) * madev(coeff[-level])
    uthresh = sigma * np.sqrt(2 * np.log(len(x)))
    coeff[1:] = (pywt.threshold(i, value=uthresh, mode='hard') for i in coeff[1:])
    return pywt.waverec(coeff, wavelet, mode='per')


def filter_signal(signal, threshold=1e8):
    fourier = rfft(signal)
    frequencies = rfftfreq(signal.size, d=1e-5)
    fourier[frequencies > threshold] = 0
    return irfft(fourier)


df_train = pd.read_csv("Wavelet Denoising\\train.csv")

df_train.head()

n_times = 1000
time = df_train['time'][:n_times].values
signal = df_train['signal'][:n_times].values


plt.figure(figsize=(15, 10))
plt.plot(time, signal)
plt.title('Signal', size=15)
plt.show()

for threshold in [1e3, 5e3, 1e4, 5e4]:
    filtered = filter_signal(signal, threshold=threshold)

    plt.figure(figsize=(15, 10))
    plt.plot(signal, label='Raw')
    plt.plot(filtered, label='Filtered')
    plt.legend()
    plt.title(f"FFT Denoising with threshold = {threshold :.0e}", size=15)
    plt.show()
