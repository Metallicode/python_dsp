import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal as sig

#normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])

sr, data = wavfile.read("guitar.wav")


#######echo FX##############
def echo(signal, time, feedback,mix=1.0,cutoff =4000):
    #create filter
    w = cutoff/(44100/2)
    a,b = sig.butter(4, w, "low", analog=False)

    #calc time in samples
    x = int(time*44100)
    d = x

    #allocate memory
    product = np.zeros_like(signal, dtype='float64')

    for i in range(feedback):
        #create empty array in length of delay time X feedback iteration
        shift = np.zeros(d)
        #concatenate <signal - tail(d)> to empty array
        delay = np.concatenate([shift, signal[:-d]*mix-(1.0/feedback)])
        #increase shift size for next iteration
        d += x
        #mix product with filtered & delayed signal
        product += sig.filtfilt(a,b,delay)

    return product

#create 'wet' signal
e= norm(echo(data, 0.3, 3, 0.7, 3000))

##plot signals
t = np.arange(0,1.0,1.0/len(data))
plt.plot(t, norm(data))
plt.plot(t, e)
plt.show()

##mix dry & wet signals
e = norm(e+norm(data))

####WRITE AUDIO FILE####
e *= 32767
e = np.int16(e)
wavfile.write("file.wav", 44100, e)


