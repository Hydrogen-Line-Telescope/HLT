import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def calibrate_data(signal_file_name, linear_ref):
    '''reference_file_name = "//home//pi//HLT_Shared//Reference_Signal_New.csv"

    referencedf = pd.read_csv(reference_file_name, header=None)
    ref = np.array(referencedf.iloc[:, 6:])
    ref = ref.flatten()

    linear_ref = []
    for i in ref:
        new_i = np.exp(i / 20)
        linear_ref.append(new_i)'''
        
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

    # print(len(filtered_sig))
    # print(len(freq))
    '''plt.plot(freq[5:-5], calibrated_signal[5:-5], label='Calibrated Data')
    plt.plot(freq[5:-5], linear_sig[5:-5], label='New Signal')
    plt.plot(freq[5:-5], linear_ref[5:-5], label='Reference Signal')
    # plt.plot(freq, filtered_sig, label='Filtered')
    # plt.xlim((freq[0], freq[-1]))
    plt.ylabel('Magnitude')
    plt.xlabel('Freq (GHz)')
    plt.legend()
    plt.title("Signal Calibration Test")
    plt.show()
    
    plt.plot(freq, calibrated_signal, label='Calibrated Data')
    # plt.plot(freq, linear_sig[5:-5], label='New Signal')
    # plt.plot(freq, linear_ref[5:-5], label='Reference Signal')
    # plt.plot(freq, filtered_sig, label='Filtered')
    # plt.xlim((freq[0], freq[-1]))
    plt.ylabel('Magnitude')
    plt.xlabel('Freq (GHz)')
    plt.legend()
    plt.title("Signal Calibration Test")
    plt.show()'''
    
    np.savetxt("//home//pi//HLT_Shared//Signal Data//RTL_LNA_Calibrated.csv", calibrated_signal, delimiter=",")

    '''print(sig)
    print(ref)'''
    return freq


def graph_reference():
    reference_file_name = "//home//pi//HLT_Shared//RTL_LNA_Reference.csv"

    referencedf = pd.read_csv(reference_file_name, header=None)
    ref = np.array(referencedf.iloc[:, 6:])
    ref = ref.flatten()

    linear_ref = []
    for i in ref:
        new_i = np.exp(i / 20)
        linear_ref.append(new_i)
        
    f0 = referencedf.iloc[0, 2]
    f1 = referencedf.iloc[-1, 3]
    df = referencedf.iloc[0, 4]

    freq = np.arange(f0, f1, df) / 1e9
        
    plt.plot(freq[5:-5], linear_ref[5:-5], label='Reference Signal')
    # plt.plot(freq, filtered_sig, label='Filtered')
    # plt.xlim((freq[0], freq[-1]))
    plt.ylabel('Magnitude')
    plt.xlabel('Freq (GHz)')
    plt.legend()
    plt.title("Reference Signal")
    plt.show()



'''reference_file_name = "//home//pi//HLT_Shared//Reference_Signal_New.csv"

referencedf = pd.read_csv(reference_file_name, header=None)
ref = np.array(referencedf.iloc[:, 6:])
ref = ref.flatten()

linear_ref = []
for i in ref:
    new_i = np.exp(i / 20)
    linear_ref.append(new_i)
        
# filter the reference signal
linear_ref = sig_proc.filter_signal(linear_ref, 1e3)'''

# calibrate_data("RTL_LNA_Array_1.csv")
# graph_reference()
