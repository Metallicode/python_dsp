import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

#normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1





###FM Part####
modulator_frequency = 5.0                  #Hz
carrier_frequency = 100.0                    #Hz

length = 1
#signal length in seconds
sr = 44100.0                                             #sample rate
t = np.arange(0,1.0,1.0/(length*sr))    #time axis

depth = 2                                                  #modulation strength
modulator = np.sin(2.0 * np.pi * modulator_frequency * t) * depth #modulator signal

product = np.zeros_like(modulator)     #allocat memory 

#generate modulated signal
for i, j in enumerate(t):
    product[i] = np.sin(2. * np.pi * (carrier_frequency * j + modulator[i]))

y = norm(product) #normalize signal 






#plot time & frequency and save to disk.....

plt.plot(t,y )
plt.plot(t, norm(modulator), color="red")
plt.show()

####PLOT SIGNAL IN FREQUENCY DOMAIN####
plt.plot(np.arange(1000),np.abs(np.fft.ifft(y))[:1000])
plt.show()

####WRITE AUDIO FILE####
y *= 32767
y = np.int16(y)
wavfile.write("file.wav", 44100, y)


