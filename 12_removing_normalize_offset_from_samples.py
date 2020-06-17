import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

#better normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)

    #fix offset
    offset = min_v+max_v
    data = data+(offset/2)

    #normalize array
    data = np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1

    #scale values and return array
    return data * ((max_v/min_v)*-1)





sr, data = wavfile.read("guitar.wav")

data = norm(data)

##plot signal
t = np.arange(0,1.0,1.0/len(data))
plt.plot(t, data)
plt.show()



