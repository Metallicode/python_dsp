import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

#normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1


samplerate, signal = wavfile.read("beat.wav")
t = np.arange(0,1.0,1.0/len(signal))
signal = norm(signal)


thd = 0.2

rms = np.zeros_like(signal)

size = 1000

for i in range(0,len(signal),size):
    s = signal[i:i+size]
    rms_i = np.sqrt(np.mean(s**2))
    if rms_i > thd:
        rms[i:i+size] = np.sqrt(np.mean(s**2))
    else:
        rms[i:i+size] = 0

rms = norm(rms)*0.5+0.5

rms = rms>thd

gated = signal*rms

plt.plot(t,gated, "black")
plt.plot(t, rms, "red")
plt.show()


####WRITE AUDIO FILE####
gated *= 32767
gated = np.int16(gated)
wavfile.write("gated_file.wav", 44100, gated)

