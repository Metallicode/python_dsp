import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal as sgl


#normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1

modulator_frequency = 50.0
carrier_frequency = 100.0
modulation_index = 5

time = np.arange(44100.0) / 44100.0
modulator = np.sin(2.0 * np.pi * modulator_frequency * time) * modulation_index

product = np.zeros_like(modulator)

for i, t in enumerate(time):
    product[i] = np.sin(2. * np.pi * (carrier_frequency * t + modulator[i]))


y = norm(product)

plt.plot(time,y )
plt.show()

####PLOT SIGNAL IN FREQUENCY DOMAIN####
plt.plot(np.arange(20000),np.abs(np.fft.ifft(y))[:20000])
plt.show()

####WRITE AUDIO FILE####
y *= 32767
y = np.int16(y)
wavfile.write("file.wav", 44100, y)


