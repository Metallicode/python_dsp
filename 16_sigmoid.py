import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal as sgl
from scipy.signal import savgol_filter


#normalize function 0-1
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])


##length will set the s width (1,1 will return a linear t), position is the s location on the x axis
def sigmoid_a(length, position=1):
    t = np.arange(-1.0*(length/2),1.0*(length/2),1.0/sample_rate) 
    y = np.zeros_like(t)
    for i in range(len(t)):
        y[i] = 1/ (1 + np.e**-t[i])

    return norm(y**position)

#speed is length of linear function, direction[up, down, bi], length of signal
def sigmoid_b(speed, direction, length):
    T = np.arange(-1.0,1.0,1.0/sample_rate)
    tq = np.arange(1,speed,1.0/sample_rate)
    
    x = np.zeros_like(T)
    for i in range(len(T)):
        x[i] = T[i]/((T[i]**2)+1)

    x = norm(x)    
   
    if direction=='up':
        new_t = np.concatenate([x[:(len(x)//2)],tq-0.5])
    elif direction=='down':
        new_t = np.concatenate([tq-0.5,x[(len(x)//2):]+speed-1])
    elif direction=='bi':
        new_t = np.concatenate([x[:(len(x)//2)],tq-0.5,x[(len(x)//2):]+speed-1])

    x = norm([new_t[i] for i  in range(len(new_t)) if i%(len(new_t)/sample_rate)==0])

    out = []
    for i in x:
        for j in range(length):
            out.append(i)

    for i in range(2):
        out = savgol_filter(out, 71, 3)
    
    return out


#x is the value at z & zb intercept. b is z curve . a is zc curve.
def sigmoid_c(length, x, b, a):
    
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

    return f



#shut up and drive...
sample_rate = 44100
frequency = 200
length = 5

##s = sigmoid_a(length,1)
##s = sigmoid_b(2, 'bi',length)
##s = sigmoid_c(length,3,4,-4)




###Sin WAVE
y = np.sin(2 * np.pi * frequency * s)

 
#y =  np.sin(2 * np.pi * frequency * y)


####WRITE AUDIO FILE####
y *= 32767
y = np.int16(y)
wavfile.write("Sigmoid_Env.wav", 44100, y)

plt.plot(range(len(s)), s)
plt.show()

