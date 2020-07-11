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
samplerate, signal = wavfile.read("count.wav")
signal = norm(np.array(signal,dtype=np.float64))

########-RMS-#########
rms = np.zeros_like(signal)
db = np.zeros_like(signal)
buffer_size = 1000

for i in range(0,len(signal),buffer_size):
    s = signal[i:i+buffer_size]
    buffer = np.sqrt(np.mean(s**2))
    rms[i:i+buffer_size] = buffer
    db[i:i+buffer_size] =  20 * np.log10(buffer)

#smooth...
cutoff = 20
normal_cutoff = cutoff / (44100/2)
b, a = butter(2, normal_cutoff, btype="low", analog=False) 
rms = filtfilt(b, a,rms)
db = filtfilt(b, a,db)

#draw
plt.subplot(211, ylabel='RMS')
plt.plot(range(len(signal)), signal, "black")
plt.plot(range(len(rms)), rms, "red")
plt.subplot(212, ylabel='dBFS')
plt.plot(range(len(db)), db, "green")
plt.show()
