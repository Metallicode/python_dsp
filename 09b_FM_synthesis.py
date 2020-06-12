import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import sounddevice

class Op():

    op_counter = 0
    
    def __init__(self, freq, gain=1.0, feed=0.0):
        self.freq = freq  
        self.gain = gain
        self.feed = feed
        self.name = f"mod_{Op.op_counter}"
        Op.op_counter += 1

    def __repr__(self):
        return f"name: {self.name}  \
freq:{self.freq}   gain:{self.gain}   \
feed:{self.feed}"

class FM_Synth():
    
    def __init__(self, f=440):
        self.sr = 44100.0
        self.time = np.arange(0,1.0,1.0/self.sr)
        self.ops = []
        self.output = Op(freq=f)
        self.signal = None

    def norm(self, data):
        min_v = min(data)
        max_v = max(data)
        return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1
            
    def create_op(self, freq, gain=1.0, feed=0.0):
        self.ops.append(Op(freq, gain, feed))

    def build(self):       
        mix = np.zeros(int(self.sr))
        
        for i in self.ops:
            #print(f"{i.freq}")
            s = np.sin(2.0 * np.pi * i.freq * (i.feed*i.freq)  * self.time) * i.gain
            mix+=s

        product = np.zeros_like(mix)

        for i, t in enumerate(self.time):
            product[i] = np.sin(2. * np.pi * (self.output.freq * t + mix[i]))

        y = self.norm(product)

        self.signal= y

    def clear(self):
        self.ops = []
        self.signal = None

    def plot(self):
        plt.plot(self.time, self.signal)
        plt.show()

    def play(self):
        sounddevice.play(self.signal, self.sr)

    def save_file(self):
        s = [i for i in self.signal]
        
        s *= 32767
        s = np.int16(s)
        wavfile.write("output.wav", self.sr, s) 
                
    def __repr__(self):
        return str([i for i in self.ops])



if __name__ == "__main__":
    from random import  randint as rnd
    import time

    synth = FM_Synth(f=100)

    while True:
        for i in range(rnd(0,5)):
            synth.create_op(freq = rnd(40,4000), gain=1.0/rnd(2,10), feed=1.0/rnd(1,3))     

        synth.build()
        synth.play()
        synth.clear()
        time.sleep(0.5)
    

##    synth.plot()
##    synth.save_file()


    
    




