import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile



#normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1

###get sample data from file
samplerate, data = wavfile.read("sample.wav")


#signal clipping
thd = 0.3
y = np.array([x/np.abs(x)-((x/np.abs(x))-(thd*x/np.abs(x))) if np.abs(x) > thd and x != 0 else x for x in signal])


##signal overdrive
drive = 5
y = norm([1-np.exp(-x*drive) if x > 0 else -1+np.exp(x*drive) for x in signal]) 



####WRITE AUDIO FILE####
y *= 32767
y = np.int16(y)
wavfile.write("clipped sample2.wav", 44100, y)




