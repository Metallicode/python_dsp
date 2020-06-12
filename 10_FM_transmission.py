import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

#normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1

###get sample data from file
samplerate, data = wavfile.read("count.wav")
t = np.arange(0,1.0,1.0/len(data))

data = np.array(data,dtype=np.float64)

###FM the sample####
FM_CARRIER = 1000.0 # Hz
MAX_DEVIATION = 10000.0 # Hz

phase = 0

product = np.zeros_like(data)

for n in range(0, len(data)):
        inputsgn = data[n] / 32768.0

        phase += inputsgn * np.pi * MAX_DEVIATION / int(samplerate)
        phase %= 2 * np.pi

        i = np.cos(phase)
        q = np.sin(phase)

        carrier = 2 * np.pi * FM_CARRIER * (n / float(samplerate))
        y = i * np.cos(carrier) - q * np.sin(carrier)
        product[n] = y

product = norm(product)

plt.plot(t,product)
plt.show()

####WRITE AUDIO FILE####
product *= 32767
product = np.int16(product)
wavfile.write("file.wav", 44100, product)




        
