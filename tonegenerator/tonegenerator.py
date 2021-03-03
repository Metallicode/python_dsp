import numpy as np
from scipy.io import wavfile
import sounddevice as sd

class Tone():
    
    def __init__(self,pitch, wavform="sin", length=0.2, sample_rate=44100):
        self.wavform = wavform
        self.length = length
        self.pitch = pitch
        self.sample_rate = sample_rate
        self.signal = None
 
    def generate(self):
        t = np.arange(0,self.length,1.0/self.sample_rate)
        x = t * np.pi * 2 * self.pitch
        if self.wavform == "sin":
            self.signal = np.sin(2 * np.pi * self.pitch * t)
        elif self.wavform == "triangle":
            self.signal = np.abs((x/np.pi-0.5)%2-1)*2-1
        elif self.wavform == "saw":
            self.signal = -((x/np.pi)%2)+1   

        sd.play(self.signal, self.sample_rate)
