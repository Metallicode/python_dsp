import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


#normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1

###get sample data from file
##samplerate, data = wavfile.read("beat.wav")
##data = norm(data)

t = np.arange(0,1.0,1.0/44100)
##t = np.arange(0,1.0,1.0/len(data))

###signal frequency
carrier_frequency = 100 #Hz
modulator_frequency = 70 #Hz

depth = 0.9
carrier = np.sin(2 * np.pi * carrier_frequency * t)
modulator = np.sin(2 * np.pi * modulator_frequency * t)*depth-(1-depth)



y = norm(carrier*modulator)

plt.plot(t, y)
plt.show()


####PLOT SIGNAL IN FREQUENCY DOMAIN####
##plt.plot(np.arange(20000),np.abs(np.fft.ifft(norm(data)))[:20000])
plt.plot(np.arange(500),np.abs(np.fft.ifft(y))[:500])
plt.show()

####WRITE AUDIO FILE####
##y *= 32767
##y = np.int16(y)
##wavfile.write("file.wav", samplerate, y)
##

