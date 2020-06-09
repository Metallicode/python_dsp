import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal


def normalize(data):
    mi = min(data)
    ma = max(data)
    return np.array([((x-mi)/(ma-mi)) for x in data])*2.0-1


sr, tone = wavfile.read("sample.wav")

cutoff =1000
w = cutoff/(44100/2)

a,b = signal.butter(4, w, "high", analog=False)
z = signal.filtfilt(a,b,tone)

a,b = signal.bessel(4, w, "high", analog=False)
q = signal.filtfilt(a,b,tone)

z = normalize(z)
q = normalize(q)

#Graph signals
plt.plot(np.arange(len(z)), normalize(tone), "orange")
plt.plot(np.arange(len(z)), z, "black")

plt.show()


####WRITE AUDIO FILE####
z *= 32767
z = np.int16(z)
wavfile.write("hp_filter.wav", sr, z)


