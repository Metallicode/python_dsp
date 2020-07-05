import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal as sgl
from scipy.signal import savgol_filter
plt.style.use('dark_background')

#normalize function 0-1
def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])

##a is the s location on the x axis, b is power of curve
def sigmoid_a(length, a=1, b=1):
    t = np.arange(-1.0*(length/2),1.0*(length/2),1.0/sample_rate) 
    sig = 1 / (a + np.exp(-t*b))
    return sig

#speed is length of linear function, direction[up, down, bi], length of signal
def sigmoid_b(speed, direction, length):
    #create -1 to 1 vector t
    T = np.arange(-1.0,1.0,1.0/sample_rate)
    #create mid linear function (sustain)
    tq = np.arange(1,speed,1.0/sample_rate)
    
    x = np.zeros_like(T)

    #create sigmoid and normalize.. SAD!
    for i in range(len(T)):
        x[i] = T[i]/((T[i]**2)+1)

    x = norm(x)    

    #concatenate functions
    if direction=='up':
        new_t = np.concatenate([x[:(len(x)//2)],tq-0.5])
    elif direction=='down':
        new_t = np.concatenate([tq-0.5,x[(len(x)//2):]+speed-1])
    elif direction=='bi':
        new_t = np.concatenate([x[:(len(x)//2)],tq-0.5,x[(len(x)//2):]+speed-1])

    #normalize again and compress x to 1 (time shift)
    x = norm([new_t[i] for i  in range(len(new_t)) if i%(len(new_t)/sample_rate)==0])

    #rescale time to length
    out = []
    for i in x:
        for j in range(length):
            out.append(i)

    #fix aliasing...  SAD!  :(
    for i in range(2):
        out = savgol_filter(out, 71, 3)
    
    return out

#x is the value at z & zb intercept. b & a are shape.
def sigmoid_c(length, x, b, a):

    #create X vector and allocate axis.
    t = np.arange(0,1.0*length,1/44100)   
    z = np.zeros_like(t)
    zb = np.zeros_like(t)
    zc = np.zeros_like(t)

    #Create first exponential function 
    Tangent_index = 0
    done = False
    for i in range(len(t)):
        z[i] = b*t[i]**2

        if t[i] >= x and done is False:
            Tangent_index = i
            done=True

    #calculate function derivative ( the sensitivity to change of the function value (output value) with respect to a change in its argument (input value))
    #gradient and tangent point
    derivative = b*2
    gradient = derivative*x
    tangent = (x, b*x**2)

    #create linear function based on gradient and tan
    for i in range(len(t)):
        zb[i] = gradient*t[i] + (tangent[1] - (gradient*tangent[0]))

    last = -1000000

    #create logarithmic function with same gradiant as zb at (0,0)
    for i in range(len(t)):
        zc[i] =  (a*t[i]**2) + (gradient*t[i]) + (tangent[1] - (gradient*tangent[0]))
        if zc[i] > last:
            last = zc[i]
        else:
            zc[i]=last

    #plot III functions
##    plt.plot(t, z)
##    plt.plot(t, zb)
##    plt.plot(t, zc)
##    plt.show()

    #concatenate functions to one vector
    delta = max(zb) + max(z[:Tangent_index])
    f = norm(np.concatenate([z[:Tangent_index], zb[Tangent_index:], zc+delta]))
    return f



########## Be Quiet And Drive... #####################
#############################################
sample_rate = 44100
frequency = 200
length = 5

s = sigmoid_a(10, 1, 2)
##s = sigmoid_b(10, 'bi',length)
##s = sigmoid_c(length,3,2,-10)


###Sin WAVE
##y = np.sin(2 * np.pi * frequency * s)

##LFO
##y =  np.sin(2 * np.pi * frequency * y)


####WRITE AUDIO FILE####
##y *= 32767
##y = np.int16(y)
##wavfile.write("Sigmoid_Env.wav", 44100, y)

plt.plot(range(len(s)), s)
plt.grid()
plt.show()

