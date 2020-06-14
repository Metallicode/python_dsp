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
carrier_frequency = 10# Hz
depth = 100.0 # Hz
signal = np.sin(2 * np.pi * carrier_frequency * t)*depth

product = np.zeros_like(data)
phase = 0

for n in range(0, len(data)):  
        product[n] = data[n+ int(signal[n])]
        

product = savgol_filter(product, 51, 3)
product = norm(product+data)



#plot signal
plt.plot(t,product)
plt.show()

####WRITE AUDIO FILE####
product *= 32767
product = np.int16(product)
wavfile.write("file.wav", 44100, product)
