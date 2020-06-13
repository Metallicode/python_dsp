import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal as sgl


#normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1

sample_rate = 44100
frequency = 5

t = np.arange(0,1.0,1.0/sample_rate)


#SAW WAVE
##product = sgl.sawtooth(2 * np.pi * frequency * t)


#SUPER SAW
##size = 1.2
##p1 = sgl.sawtooth(2 * np.pi * (frequency-size) * t)
##p2 = sgl.sawtooth(2 * np.pi * (frequency+size) * t)
##y = norm(product+p1+p2)


#triangle...
product = sgl.sawtooth(2 * np.pi * frequency * t, 0.5)

##Sweep
##p = np.poly1d([0.2,0.3,0.4,0.5,0.6,8])
##t = np.linspace(0, 10, sample_rate)
##w = sgl.sweep_poly(t, p)

y = norm(product)


plt.plot(t,y)

####PLOT SIGNAL IN FREQUENCY DOMAIN####
##plt.plot(np.arange(20000),np.abs(np.fft.ifft(y))[:20000])
plt.show()

####WRITE AUDIO FILE####
y *= 32767
y = np.int16(y)
wavfile.write("file.wav", 44100, y)


