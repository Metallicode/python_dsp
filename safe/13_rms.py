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

##frequency = 5 #Hz
##signal = np.sin(2 * np.pi * frequency * t)


rms = np.zeros_like(signal)

size = 1000

for i in range(0,len(signal),size):
    s = signal[i:i+size]
    rms[i:i+size] = np.sqrt(np.mean(s**2))


plt.plot(t, signal, "black")
plt.plot(t, rms, "red")
plt.show()
