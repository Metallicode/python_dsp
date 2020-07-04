import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

#normalize function 0-1
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])

#x is the value at z & zb intercept. p is z curve power. b is z volume (sustain length?). a is zc curve.
def func(length, x, b, a):
    
    t = np.arange(0,1.0*length,1/44100)   
    z = np.zeros_like(t)
    zb = np.zeros_like(t)
    zc = np.zeros_like(t)

    hashaka_index = 0
    done = False
    for i in range(len(t)):
        z[i] = b*t[i]**2

        if t[i] >= x and done is False:
            hashaka_index = i
            done=True
  
    nigzeret = b*2
    shipoa = nigzeret*x

    nekodat_hashaka = (x, b*x**2)

    for i in range(len(t)):
        zb[i] = shipoa*t[i] + (nekodat_hashaka[1] - (shipoa*nekodat_hashaka[0]))

    last = -1000
    for i in range(len(t)):
        zc[i] =  (a*t[i]**2) + (shipoa*t[i]) + (nekodat_hashaka[1] - (shipoa*nekodat_hashaka[0]))
        if zc[i] > last:
            last = zc[i]
        else:
            zc[i]=last
        
##    plt.plot(t, z)
##    plt.plot(t, zb)
##    plt.plot(t, zc)
##    plt.show()

    delta = max(zb) + max(z[:hashaka_index])

    f = norm(np.concatenate([z[:hashaka_index], zb[hashaka_index:], zc+delta]))
    plt.plot(range(len(f)), f)
    plt.show()

    return f

#shut up and drive...
length = 3

s = func(length,0.5,4,-4)


y =  np.sin(2 * np.pi * 500 * s)



####WRITE AUDIO FILE####
y *= 32767
y = np.int16(y)
wavfile.write("fileenv.wav", 44100, y)

