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

def segments(keyframes, First=True):
    if First == True:
        return [(keyframes[i],keyframes[i+1]) for i in range(0,len(keyframes)-1,2)]
    else:
        return [(keyframes[i],keyframes[i+1]) for i in range(1,len(keyframes)-1,2)]

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

#calculate_dynamics 
threshold = 0.05
keyframes = calculate_dynamics(rms, threshold)


#commpression power
ratio = 1.2
bias = -0.2
speed = 80
makeup_gain =1

min_rms = min(rms)

c = np.zeros_like(rms)
gr = np.zeros_like(rms)

compression = (-rms*ratio)+(1-(min_rms+threshold))

for segment in segments(keyframes, False):
    gr[segment[0]:segment[1]] = ((rms[segment[0]:segment[1]]-bias)*(-1*norm(np.cosh(np.linspace(-speed,speed,segment[1]-segment[0])), True)+1))
    for i in range(segment[0],segment[1],buffer_size):
        s = gr[i:i+buffer_size]*-1+1
        c[i:i+buffer_size] = signal[i:i+buffer_size] * s

for segment in segments(keyframes):
    for i in range(segment[0],segment[1],buffer_size):
        c[i:i+buffer_size] = signal[i:i+buffer_size]

c = norm(c)*makeup_gain





#draw
plt.plot(range(len(signal)), signal, "black")

plt.plot(range(len(signal)), c, "pink")
plt.plot(range(len(compression)), compression*-1+1-threshold, "red", dashes=[6, 2])
plt.plot(range(len(signal)), gr*-1+1, "blue")
plt.axhline(y=threshold, color ="green")

for i in range(len(keyframes)):
    plt.axvline(x=keyframes[i], color ="yellow")

for v in segments(keyframes):
    plt.axvspan(v[0],v[1], facecolor='0.2', alpha=0.5)

for v in segments(keyframes, False):
    plt.axvspan(v[0],v[1], facecolor='0.5', alpha=0.2)


plt.show()



#write file
c *= 32767
c = np.int16(c)
wavfile.write("file.wav", 44100, c)

