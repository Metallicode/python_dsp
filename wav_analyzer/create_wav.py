from datetime import datetime
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

class wave_maker:
    
    def __init__(self, length=1.0 , sampleRate=44100):
        self.length = length
        self.sr = sampleRate     

    def _norm(self, data):
        min_v = min(data)
        max_v = max(data)

        offset = min_v+max_v
        data = data+(offset/2)

        data = np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1

        return data * ((max_v/min_v)*-1)

    
    def _wav_fragmentation(self, signal):
        num_of_breaks = random.randint(1,100)
        list_of_breaks = []

        step_size = self.sr//num_of_breaks
        counter = 0
        
        for i in range(num_of_breaks):
            list_of_breaks.append((random.randint(1+counter ,counter+step_size),
                                   random.randint(1+counter+step_size ,(step_size*2)+counter)))
            counter += step_size
        new_buffer = np.zeros_like(signal)

        for i in range(len(list_of_breaks)):
            signal[list_of_breaks[i][0]:list_of_breaks[i][1]] = 0

        return signal

    def make_signal(self):
        t = np.arange(0,self.length,1/self.sr)
        sig01 = np.sin(2 * np.pi * random.randint(20, 20000) * t)
        sig02 = np.sin(2 * np.pi * random.randint(20, 20000) * t)
        sig03 = np.sin(2 * np.pi * random.randint(20, 20000) * t)
        noise = 0.2 * np.random.randn(*sig01.shape)

        complex_wav = sig01+sig02+sig03+noise
        return self._norm(self._wav_fragmentation(complex_wav))


    def make_wav_file(self, signal):
        new = [x*32767 for x in signal]
        new = np.int16(new)
        wavfile.write(f"file.wav", self.sr, new)
        return signal

if __name__ == "__main__":
    w = wave_maker()
    w.make_wav_file(w.make_signal())




