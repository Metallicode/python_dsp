import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

#normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1

###SET sample rate & signal frequency
sample_rate = 44100
frequency = 80 #Hz

t = np.arange(0,1.0,1.0/sample_rate)

####PRODUCE SIGNALS
#signal = np.sin(2 * np.pi * frequency * t)
signal = (np.mod(frequency*t,1) < 0.5)*2.0-1
noise = 1.0*np.random.randn(*signal.shape)

####COMBINE NOISE AND SIGNAL (and normalize array...)
dirty =  norm(signal+noise)

####PLOT SIGNAL####
plt.plot(t, dirty,'orange');
plt.show()

####WRITE AUDIO FILE####
##signal *= 32767
##signal = np.int16(signal)
##wavfile.write("file.wav", sample_rate, signal)
