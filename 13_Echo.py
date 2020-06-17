import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal as sig

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



#######echo FX##############
def echo(signal, bpm, feedback,mix=1.0,cutoff =4000):
    #create filter
    w = cutoff/(44100/2)
    a,b = sig.butter(4, w, "low", analog=False)

    #calc time in samples
    x = round(1/bpm * 60 * 44100)
    d = x

    #allocate memory
    product = np.zeros_like(signal, dtype='float64')
    

    for i in range(feedback):
        #create empty array in length of delay time X feedback iteration
        shift = np.zeros(d)
        #concatenate <signal - tail(d)> to empty array
        delay = np.concatenate([shift, signal[:-d]*(1.0/(i+1))])
        #increase shift size for next iteration
        d += x
        #mix product with filtered & delayed signal
        product += sig.filtfilt(a,b,delay)

    return norm(product)*mix



#create 'wet' signal
e= echo(data, 300 ,10 , 0.5, 3000)




##plot signals
t = np.arange(0,1.0,1.0/len(data))
plt.plot(t, data)
plt.plot(t, e)
plt.show()



##mix dry & wet signals
e = norm(e+data)



####WRITE AUDIO FILE####
e *= 32767
e = np.int16(e)
wavfile.write("file.wav", 44100, e)


