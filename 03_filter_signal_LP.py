import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


def LPF(data,alpha):
    yi = 0
    y = []
    for i in range(len(data)):
        yi += alpha*(data[i]-yi)
        y.append(yi)
    return y

#normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1



###SET sample rate & signal frequency
sample_rate = 44100
frequency = 5 #Hz

t = np.arange(0,1.0,1.0/sample_rate)

####PRODUCE SIGNALS
#signal = np.sin(2 * np.pi * frequency * t)
signal = (np.mod(frequency*t,1) < 0.5)*2.0-1
noise = 1.0*np.random.randn(*signal.shape)

####COMBINE NOISE AND SIGNAL (and normalize array...)
#dirty =  norm(signal+noise)

sr, data = wavfile.read("sample.wav")

dirty = norm(data)


cutoff = 5
alpha = cutoff / (sample_rate/2)




####PLOT SIGNAL IN FREQUENCY DOMAIN####
##plt.plot(np.arange(20000),np.abs(np.fft.ifft(norm(data)))[:20000])
##plt.plot(np.arange(20000),np.abs(np.fft.ifft(dirty))[:20000])
##
##plt.show()

####WRITE AUDIO FILE####
dirty *= 32767
dirty = np.int16(dirty)
wavfile.write("filed.wav", sample_rate, dirty)
