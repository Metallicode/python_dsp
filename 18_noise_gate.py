
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter,filtfilt

#normalize function
def norm(data, simple=False):
    min_v = min(data)
    max_v = max(data)
    if simple is False:
        offset = min_v+max_v
        data = data+(offset/2)
        data = np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1
        return data * ((max_v/min_v)*-1)
    else:
        return np.array([((x-min_v) / (max_v-min_v)) for x in data]) 

def flat_edge(arr,keyframes, intro=True):
    if intro:
        a = keyframes[0]
        b = keyframes[1]
    else:
        a = keyframes[-2]
        b = keyframes[-1]        
    
    for i in range(a,b):
        arr[i] = 0
    return arr

def gates(signal, segments, speed= 50):
    ones = np.ones_like(signal)
    for s in segments:
        ones[s[0]:s[1]] = norm(np.cosh(np.linspace(-speed,speed,s[1]-s[0])), True)
    return ones

def segments(keyframes, First=True):
    if First == True:
        return [(keyframes[i],keyframes[i+1]) for i in range(0,len(keyframes)-1,2)]
    else:
        return [(keyframes[i],keyframes[i+1]) for i in range(1,len(keyframes)-1, 2)]

def calculate_dynamics(rms, threshold):
    keyframes = [0]
    lastkeyframewasUp = False

    for i in range(len(rms)):  
        if  rms[i] <  threshold:
            if lastkeyframewasUp == True:
                keyframes.append(i)
                lastkeyframewasUp = False
        else:
             if lastkeyframewasUp == False:
                keyframes.append(i)
                lastkeyframewasUp = True

    keyframes.append(len(signal))

    if keyframes[1] == 0:
        del keyframes[0]
    return keyframes
    


#read file
samplerate, signal = wavfile.read("count.wav")
signal = norm(np.array(signal,dtype=np.float64))

########-RMS-#########
rms = np.zeros_like(signal)
buffer_size = 1000

for i in range(0,len(signal),buffer_size):
    s = signal[i:i+buffer_size]
    rms[i:i+buffer_size] = np.sqrt(np.mean(s**2))
 
#smooth...
cutoff = 20
normal_cutoff = cutoff / (44100/2)
b, a = butter(2, normal_cutoff, btype="low", analog=False) 
rms = filtfilt(b, a,rms)

# calculate gate
threshold = 0.2
flip_order = True

keyframes = calculate_dynamics(rms, threshold)
g = gates(signal, segments(keyframes, flip_order), 50)

### flate edges #####
g = flat_edge(g, keyframes, True)
g = flat_edge(g, keyframes, False)


## gate signal
gated = signal*g

######## Draw ##########
plt.plot(range(len(signal)), signal, "black")
plt.plot(range(len(signal)), gated, "pink")

plt.plot(range(len(signal)), g, "yellow")
plt.plot(range(len(signal)), rms, "red")

plt.axhline(y=threshold, color ="green")

plt.show()


#write to file
gated *= 32767
gated = np.int16(gated)
wavfile.write("file.wav", 44100, gated)


