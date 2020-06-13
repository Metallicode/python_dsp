import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

#normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1

###get sample data from file
samplerate, data = wavfile.read("beat.wav")
t = np.arange(0,1.0,1.0/len(data))
data = np.array(data,dtype=np.float64)
data = norm(data)




###FM the sample####
carrier_frequency = 100.0 # Hz
depth = 5000.0 # Hz

product = np.zeros_like(data)
phase = 0

for n in range(0, len(data)):  
        phase += data[n] * np.pi * depth / int(samplerate)
        phase %= 2 * np.pi

        carrier = 2 * np.pi * carrier_frequency * (n / float(samplerate))
        
        product[n] = np.cos(phase) * np.cos(carrier) - np.sin(phase) * np.sin(carrier)


product = norm(product)





#plot signal
plt.plot(t,product)
plt.show()

####WRITE AUDIO FILE####
product *= 32767
product = np.int16(product)
wavfile.write("file.wav", 44100, product)
