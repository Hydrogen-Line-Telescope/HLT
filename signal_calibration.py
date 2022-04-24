import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from numpy.fft import rfft, rfftfreq, irfft


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


def calibrate_data(signal_file_name):
    reference_file_name = "Z:\\Reference_Signal_New.csv"
    '''Z:\\Reference_Signal.csv"'''

    referencedf = pd.read_csv(reference_file_name, header=None)
    ref = np.array(referencedf.iloc[:, 6:])
    ref = ref.flatten()

    linear_ref = []
    for i in ref:
        new_i = np.exp(i / 20)
        linear_ref.append(new_i)

    linear_ref = np.array(linear_ref)

    linear_ref = filter_signal(linear_ref, 1e4)

    signaldf = pd.read_csv(signal_file_name, header=None)
    sig = np.array(signaldf.iloc[:, 6:])
    sig = sig.flatten()

    linear_sig = []
    for i in sig:
        new_i = np.exp(i / 20)
        linear_sig.append(new_i)

    calibrated_signal = np.subtract(linear_sig, linear_ref)

    # graphing for testing
    f0 = signaldf.iloc[0, 2]
    f1 = signaldf.iloc[-1, 3]
    df = signaldf.iloc[0, 4]

    freq = np.arange(f0, f1, df) / 1e9

    freq = freq[100:-100]
    # print(len(filtered_sig))
    # print(len(freq))
    calibrated_signal = np.array(calibrated_signal)

    calibrated_signal = filter_signal(calibrated_signal, 1e4)
    calibrated_signal = calibrated_signal[100:-100]
    plt.plot(freq, calibrated_signal, label='Calibrated Data')
    #plt.plot(freq, linear_sig[100:-100], label='New Signal')
    #plt.plot(freq, linear_ref[100:-100], label='Reference Signal')
    # plt.plot(freq, filtered_sig, label='Filtered')
    # plt.xlim((freq[0], freq[-1]))
    plt.ylabel('Magnitude')
    plt.xlabel('Freq (GHz)')
    plt.legend()
    plt.title("Signal Calibration Test")
    plt.show()

    '''print(sig)
    print(ref)'''


'''calibrate_data('C:\\Users\\jojok\\PycharmProjects\\pythonProject\\HLT\\Results\\Results Apr-24-2022 16-18-24\\Data '
               'Files\\raw_signal_data.csv')'''
