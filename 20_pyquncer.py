import numpy as np
from scipy.io import wavfile

def prog(hz, length):
    t = np.arange(0,length,1.0/sample_rate)
    signal = np.sin(2 * np.pi * hz * t)
    return list(signal)
    
sample_rate = 44100


list_of_hz = [690,78,764,234,876,2000,100,234]
list_of_lengths = [0.2,0.1,0.5,0.4,0.6,0.2,0.1,0.2]


new_melody = []


for i in range(len(list_of_hz)):
    new_melody+=prog(list_of_hz[i], list_of_lengths[i])

new_melody = np.array(new_melody*5)



####FM it
t = np.arange(0,len(new_melody)/sample_rate,1.0/sample_rate)
new_melody = np.sin(2 * np.pi * 5 * new_melody * t)


##WRITE AUDIO FILE####
new_melody *= 32767
new_melody = np.int16(new_melody)
wavfile.write("file.wav", sample_rate, new_melody)
