import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter,filtfilt

#normalize function
def norm(data):
    min_v = min(data)
    max_v = max(data)

    offset = min_v+max_v
    data = data+(offset/2)

    data = np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1

    return data * ((max_v/min_v)*-1)


#read file
samplerate, signal = wavfile.read("count.wav")
signal = norm(np.array(signal,dtype=np.float64))


########-RMS-#########
rms = np.zeros_like(signal)
buffer_size = 1000

threshold = 0.005

keyframes = [0]
lastkeyframewasUp = False

for i in range(0,len(signal),buffer_size):
    s = signal[i:i+buffer_size]
    rms[i:i+buffer_size] = np.sqrt(np.mean(s**2))
    
    if  rms[i] <  threshold:
        if lastkeyframewasUp == True:
            keyframes.append(i)
            lastkeyframewasUp = False
    else:
         if lastkeyframewasUp == False:
            keyframes.append(i)
            lastkeyframewasUp = True

keyframes.append(len(signal))

lst = [(keyframes[x],keyframes[x+1]) for x in range(0,len(keyframes)-1)]

#smooth...
cutoff = 20
normal_cutoff = cutoff / (44100/2)
b, a = butter(2, normal_cutoff, btype="low", analog=False) 
rms = filtfilt(b, a,rms)


#draw
plt.plot(range(len(signal)), signal, "black")
plt.plot(range(len(rms)), rms, "red")
plt.axhline(y=threshold, color ="green")

for i in range(len(lst)):
    plt.axvline(x=lst[i][0], color ="yellow")
    if i%2 ==0:
        plt.axvspan(lst[i][0],lst[i][1], facecolor='0.2', alpha=0.5)

plt.show()
