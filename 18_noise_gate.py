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

def gates(signal, segments, speed= 50):
    ones = np.ones_like(signal)
    for s in segments:
        t = np.linspace(-speed,speed,s[1]-s[0])
        hyper_s = np.sinh(t)
        window = (hyper_s*hyper_s)
        ones[s[0]:s[1]] = norm(window, True)
    return ones

def segments(keyframes, First=True):
    if First == True:
        return [(keyframes[i],keyframes[i+1]) for i in range(0,len(keyframes)-1,2)]
    else:
        return [(keyframes[i],keyframes[i+1]) for i in range(1,len(keyframes)-1, 2)]

def calculate_dynamics(rms, threshold):
    keyframes = []
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
    return keyframes
    





#read file
samplerate, signal = wavfile.read("beat.wav")
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

#gate
threshold = 0.2
keyframes = calculate_dynamics(rms, threshold)
g = gates(signal, segments(keyframes, False), 50)
gated = signal*g

#draw
plt.plot(range(len(signal)), signal, "black")
plt.plot(range(len(signal)), gated, "pink")

plt.plot(range(len(signal)), g, "yellow")
plt.plot(range(len(rms)), rms, "red")
plt.axhline(y=threshold, color ="green")

plt.show()

gated *= 32767
gated = np.int16(gated)
wavfile.write("file.wav", 44100, gated)


