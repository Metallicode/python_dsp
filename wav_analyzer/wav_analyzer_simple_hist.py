import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from create_wav import wave_maker

def _burst(signal, index):
    counter = 0
    for i in range(index,len(signal)):
        if signal[i] == signal[index]:
            counter +=1
        else:
            break
    return counter

def analyze(signal, min_burst_length = 1):
    counter = 0
    bursts_indexes = []

    while counter<len(signal):
        if signal[counter] == 0.0:
            burst_size = _burst(signal, counter)
            bursts_indexes.append((counter, counter+burst_size))
            
            if burst_size > min_burst_length:
                counter += burst_size                
        else:
            counter+=1
    return bursts_indexes


if __name__ == "__main__":
    
    sr, data = wavfile.read("file.wav")
    output = analyze(data)

    lengths = [x[1]-x[0] for x in output]

    plt.hist(lengths, bins = 100)
    plt.show()
    


        
        
