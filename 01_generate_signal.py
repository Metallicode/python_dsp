import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

sample_rate = 44100
frequency = 4

t = np.arange(0,1.0,1.0/sample_rate)

signal = np.sin(2 * np.pi * frequency * t)

#signal = (np.mod(frequency*t,1) < 0.5)*2.0-1
#noise = 1.0*np.random.randn(*signal.shape)

####PLOT SIGNAL####
##plt.plot(t, signal,'black')
##plt.plot(t, signal+noise,'orange');
##plt.show()



####WRITE AUDIO FILE####
##signal *= 32767
##signal = np.int16(signal)
##wavfile.write("file.wav", sample_rate, signal)
