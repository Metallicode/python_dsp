import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile




def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1



###get sample data from file
samplerate, data = wavfile.read("beat.wav")
data = norm(data)

q = 0.8
y = q* np.round(data/q)

plt.plot(np.arange(len(data)),data)
plt.show()

####WRITE AUDIO FILE####
y *= 32767
y = np.int16(y)
wavfile.write("file.wav", 44100, y)

