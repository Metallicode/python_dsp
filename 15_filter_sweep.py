import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter,filtfilt
from scipy import signal as sgl
from scipy.io import wavfile

def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1

def split_signal(signal, step, size):
    return  [signal[i : i + size] for i in range(0, len(signal), step)]

def heal(chunks, x_len):
    x = chunks[0]
    for i in range(0,len(chunks)-1):
        x= merge(x, chunks[i+1], x_len)    
    return x

def merge(a,b, overlap):  
    return list(a[:-overlap]) + cross_fade(a[len(a)-overlap:], b[:overlap]) + list(b[overlap:] )

def cross_fade(a,b):
    newlst = []
    lin = [x/10 for x in range(0,len(a))]
    for i in range(len(a)):
        newlst.append((a[i]*lin[::-1][i]) + (b[i]*lin[i]))
    return newlst


def filter_sweep(signal, hi_freq, order = 5, step=1000, upsweep=True):
    p = split_signal(signal, step, step*2)
    env = np.array([k for k in np.linspace(10,hi_freq, len(p))])
    
    x = []
    
    for i in range(0, len(p)-1):
        cutoff = env[i] if upsweep else env[::-1][i]
        normal_cutoff = cutoff / (44100/2)
        b, a = butter(order, [normal_cutoff, normal_cutoff+0.2], btype="band", analog=False) 
        x.append(filtfilt(b, a,p[i]))

    x = heal(x, step)
    return x


##create signal
sample_rate = 44100
frequency = 90
note_length = 10
t = np.arange(0,1.0*note_length,1.0/sample_rate,  dtype='float64')
product = sgl.sawtooth(2 * np.pi * frequency * t)


##Filter the signal
product = np.array(filter_sweep(product, 5000))

##Normalize......
x = norm(product)[::-1]

##Plot
plt.plot([i for i in range(len(x))],x)
plt.show()

##Write to file
x *= 32767
x = np.int16(x)
wavfile.write("file.wav", 44100, x)
