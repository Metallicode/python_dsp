import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter,filtfilt

#normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)

    offset = min_v+max_v
    data = data+(offset/2)

    data = np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1

    return data * ((max_v/min_v)*-1)


#read file
samplerate, signal = wavfile.read("guitar.wav")
signal = norm(signal)



########-RMS-#########
rms = np.zeros_like(signal)
buffer_size = 1000

for i in range(0,len(signal),buffer_size):
    s = signal[i:i+buffer_size]
    rms[i:i+buffer_size] = np.sqrt(np.mean(s**2))


#smooth...
cutoff = 20
normal_cutoff = cutoff / (44100/2)
b, a = butter(2, normal_cutoff, btype="low", analog=False) 
rms = filtfilt(b, a,rms)



#draw
plt.plot(range(len(signal)), signal, "black")
plt.plot(range(len(rms)), rms, "red")
plt.axhline(y=0.05, color ="green")
plt.show()
