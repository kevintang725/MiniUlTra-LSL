import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from tqdm import tqdm
from scipy.signal import butter, filtfilt
import padasip as pa

# Functions
class Data_Properties():
    def __init__(self):
        self.time = []
        self.y_DC = []
        self.trigger = []
        self.FFT = []
        self.freq = []
        self.epochs = []

def butter_highpass_filter(data, cutoff, fs, order):
    normal_cutoff = cutoff / (0.5*fs)
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = filtfilt(b, a, data)
    return y

def butter_lowpass_filter(data, cutoff, fs, order):
    normal_cutoff = cutoff / (0.5*fs)
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def linear_interpolation(x1, y1, x2, y2):
    output = y1 + (x2 - x1)*((y2 - y1)/(x2 - x1))
    return output

def extract_epochs(x, y, length, trigger):
    epoch_data = np.array([])
    epoch_time = np.array([])
    for i in range(length):
        if trigger[i] == 1:
            epoch_loc = i
            start = int(epoch_loc-math.floor((100/(1/fs)/1000)))
            end = int(epoch_loc+math.floor((600/(1/fs)/1000)))
            epoch_data = np.hstack((epoch_data, y[start:end]))
            epoch_time = np.hstack((epoch_time, x[start:end]))
            #print(epoch_loc)
    epoch_samples = end-start
    try:
        X = np.reshape(epoch_time,(epoch_samples,-1))
        Y = np.reshape(epoch_data,(epoch_samples,-1))
    except:
        X = epoch_time[0:epoch_samples*math.floor((len(epoch_time)/(epoch_samples)))]
        X = np.reshape(X, (epoch_samples, -1))

        Y = epoch_data[0:epoch_samples*math.floor((len(epoch_data)/(epoch_samples)))]
        Y = np.reshape(Y, (epoch_samples, -1))
    return X, Y

def read_file(pathfile,fs):
    fc1 = 5      # desired cutoff frequency of the filter, Hz 
    fc2 = 200      # desired cutoff frequency of the filter, Hz 
    order = 2       # sin wave can be approx represented as quadratic

    channel_sel = 1

    df = pd.read_csv(pathfile)

    # Initialize Vectors
    time = []
    data = []

    # Define signal of interest in time
    start = 10000
    stop = start + 2000
    step = 1

    # Reformat and Clean Data to Float Array
    for i in tqdm(range(start,stop,step) ,"Importing Data..."):
    # Convert to numpy format
        df_numpy = df.to_numpy()

        data_string_array = df_numpy[i,2]   # Access individual data string per time index
        data_string_array = (data_string_array[1:-1].split(','))  # Split data string to list
        float_array = [float(string) for string in data_string_array]    # Convert data string list to data float list
        data.append(np.array(float_array))  # Re-format as numpy array for data
        time.append(np.array(float(df_numpy[i,1]))) # Re-format as numpy array for time

    # Package data for processing
    D = np.array(data)
    trigger = D[:,56]   # Trigger Channel 56
    data = 1e6*D # Convert to uV
    time = np.array(time) - min(time)

    # Filter DC Bias
    y_DC = butter_highpass_filter(data[:,channel_sel], fc1, fs, order)
    y_DC = butter_lowpass_filter(y_DC, fc2, fs, order)

    # Calculate PSD
    FFT = np.fft.fft(y_DC)
    freq = np.fft.fftfreq(time.shape[-1])

    return time, y_DC, trigger, FFT, freq

# Filter requirements.
fs = 512       # sample rate, Hz

# Read CSV as Dataframe
control = "/Users/KevinTang/Desktop/UTAustin/Code/GitHub/Human Trials/FUS + EEG (SEP)/JL_08172023/JL_FUS-FES-_1.csv"
NG1 = "/Users/KevinTang/Desktop/UTAustin/Code/GitHub/Human Trials/FUS + EEG (SEP)/JL_08172023/JL_FUS+FES-_1_.csv"
NG2 = "/Users/KevinTang/Desktop/UTAustin/Code/GitHub/Human Trials/FUS + EEG (SEP)/JL_08172023/JL_FUS+FES-_2.csv"


# Initialize Classes
CTRL = Data_Properties()
TRAIN = Data_Properties()
VAL = Data_Properties()


# Analyze
CTRL.time, CTRL.y_DC, CTRL.trigger, CTRL.FFT, CTRL.freq = read_file(control, fs)
TRAIN.time, TRAIN.y_DC, TRAIN.trigger, TRAIN.FFT, TRAIN.freq = read_file(NG1, fs)
VAL.time, VAL.y_DC, VAL.trigger, VAL.FFT, VAL.freq = read_file(NG2, fs)

# Extract Epochs
CTRL.epochst, CTRL.epochs = extract_epochs(CTRL.time, CTRL.y_DC, len(CTRL.y_DC), CTRL.trigger)
TRAIN.epochst, TRAIN.epochs = extract_epochs(TRAIN.time, TRAIN.y_DC, len(TRAIN.y_DC), TRAIN.trigger)
VAL.epochst, VAL.epochs = extract_epochs(VAL.time, VAL.y_DC, len(VAL.y_DC), VAL.trigger)


## Adaptive Filter LMS
x = TRAIN.epochs
d = np.mean(CTRL.epochs, axis = 1)
n_epochs = x.shape[1]
print('Input Dimension: ' + str(x.shape))
print('Target Dimension: ' + str(d.shape))
f = pa.filters.FilterNLMS(n= n_epochs, mu=1, w="random")
y, e, w = f.run(d, x)

# Evaluate Ad-Hoc ADP_NLMS Filter
x_train = np.mean(TRAIN.epochst, axis=1)
y_train = np.mean(TRAIN.epochs, axis=1)
x_ctrl = np.mean(CTRL.epochst, axis = 1)
y_ctrl = np.mean(CTRL.epochs, axis = 1)

y_FFT = np.fft.fft(y)
y_freq = np.fft.fftfreq(CTRL.epochst.shape[0])

freq_train = TRAIN.freq
FFT_train = TRAIN.FFT
freq_ctrl = CTRL.freq
FFT_ctrl = CTRL.FFT


plt.figure(figsize=(15,9))

plt.subplot(2,2,1)
plt.plot(x_train, y_train,"b", label="FUS Contaminated Signal")
plt.plot(x_ctrl, y_ctrl,"r", label="Adaptive Filtered Signal")
plt.legend()
plt.xlabel('Time (s)')
plt.ylabel('Voltage (uV)')
plt.title('Adaptive Filter')

plt.subplot(2,2,2)
print(y_freq.shape)
print(y_FFT.shape)
plt.loglog(fs*freq_train[0:math.floor(len(freq_train)/2)], abs(FFT_ctrl[0:math.floor(len(FFT_ctrl)/2)]),"b", label="FUS Contaminated Signal")
plt.loglog(fs*y_freq[0:math.floor(len(y_freq)/2)], abs(y_FFT[0:math.floor(len(y_FFT)/2)]),"r", label="Adaptive Filtered Signal (Training)")
plt.legend()
plt.xlabel('Frequency (Hz)')
plt.ylabel('PSD ($uV^{2}$ $Hz^{-1}$)')
plt.xlim([1, 100])
plt.title('PSD')

plt.subplot(2,2,3);plt.title("Adaptation");plt.xlabel("samples - k")
plt.plot(d,"b", label="Target (FUS-FES-)")
plt.plot(y,"r", label="ADP_NLMS (Adaptive Filtered Signal)");plt.legend()

#plt.subplot(2,2,4);plt.title("Filter error");plt.xlabel("samples - k")
#plt.plot(10*np.log10(e**2),"r", label="e - error [dB]");plt.legend()
# Use
plt.show()



