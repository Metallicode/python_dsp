import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal as sgl


class Evnelope:
    def __init__(self,strength=1.0, length=44100, log=0.0):
        lst = [(x**log//length) for x in reversed(range(length))]
        max_v = max(lst)
        self.env = np.array([x/ max_v for x in lst])*strength
        


sample_rate = 44100
frequency = 100

t = np.arange(0,1.0,1.0/sample_rate)

e = Evnelope(strength=1.3, log=79).env



#Sin WAVE
y = np.sin(2 * np.pi * frequency * e)


plt.plot(t,y)
plt.plot(t,e)

plt.show()

####WRITE AUDIO FILE####
y *= 32767
y = np.int16(y)
wavfile.write("fileenv.wav", 44100, y)


