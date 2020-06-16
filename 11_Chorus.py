import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import savgol_filter


#normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1

###get sample data from file
samplerate, data = wavfile.read("guitar.wav")
t = np.arange(0,1.0,1.0/len(data))
data = np.array(data,dtype=np.float64)
data = norm(data)

###Chorus FX####
mod_frequency = 7.0 #Hz
depth = 100.0

lfo = np.sin(2*np.pi * t * mod_frequency)*depth


product = np.zeros_like(data)


for i in range(0, len(data)):
    product[i] = data[i + int(lfo[i])]


product = savgol_filter(product, 51, 3)

product = norm(data + product)



#plot signal
plt.plot(t,product)
plt.show()

####WRITE AUDIO FILE####
product *= 32767
product = np.int16(product)
wavfile.write("chorus_out.wav", 44100, product)
