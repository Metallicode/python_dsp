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
frequency = 100
note_length = 2
t = np.arange(0,1.0*note_length,1.0/sample_rate)


def cloud_maker(freq , n, diff, t, octaver=True):
    product = sgl.sawtooth(2 * np.pi * freq * t)
    
    for i in range(n):
        product += sgl.sawtooth(2 * np.pi * (freq-diff) * t)
        product += sgl.sawtooth(2 * np.pi * (freq+diff) * t)
        diff += diff
        product = norm(product)
    if octaver == True:
        product += sgl.sawtooth(2 * np.pi * freq/2 * t)
        product += sgl.sawtooth(2 * np.pi * freq/4 * t)*0.5
    return product






#SAW WAVE
product = cloud_maker(frequency, 20, 0.000001, t)

y = norm(product)






####PLOT SIGNAL IN FREQUENCY DOMAIN####
plt.plot(np.arange(4000),np.abs(np.fft.ifft(y))[:4000])

#plt.plot(t,y)
plt.show()

####WRITE AUDIO FILE####
y *= 32767
y = np.int16(y)
wavfile.write("file.wav", 44100, y)


