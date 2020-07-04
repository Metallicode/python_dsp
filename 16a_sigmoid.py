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


#shut up and drive...
sample_rate = 44100
frequency = 50
length = 10

q = sigmoid_a(length,1)
##q = sigmoid_b(5, 'bi',length)

plt.plot(range(len(q)), q)
plt.show()

y = np.sin(2 * np.pi * 1000 * q)

##s = sigmoid(0.5, 'up', length)


###Sin WAVE
##y = np.sin(2 * np.pi * 1550 * s)


##y =  np.sin(2 * np.pi * frequency * y * s)



####WRITE AUDIO FILE####
y *= 32767
y = np.int16(y)
wavfile.write("fileenv.wav", 44100, y)

##plt.plot(range(len(s)), s)
##plt.show()
