import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from create_wav import wave_maker

class analysys:
    def __init__(self, signal, locations, sr=44100):
        self.locations = locations
        self.numofkrechtz = len(locations)
        self.signal = signal
        self.sr = sr

    def __repr__(self):
        return f"Krechtz count in signal: {self.numofkrechtz}\n Krechtz index: {self.locations}"

    def show(self):
        plt.plot(np.arange(0,self.sr*(len(self.signal)/self.sr),1) , self.signal)
        locs = [item for t in self.locations for item in t] 
        for i in range(len(locs)):
            if i%2 == 0:
                plt.axvspan(locs[i], locs[i+1], facecolor='0.05', alpha=0.5)
            plt.axvline(x=locs[i], color ="red")

        plt.show()

    

class wave_analyzer: 
    def __init__(self, signal):
        self.signal = signal

    def _burst(self, index):
        counter = 0
        for i in range(index,len(self.signal)):
            if self.signal[i] == self.signal[index]:
                counter +=1
            else:
                break
        return counter
        
    def analyze(self, min_burst_length = 0):
        counter = 0
        bursts_indexes = []

        while counter<len(self.signal):
            if self.signal[counter] == 0.0:
                burst_size = self._burst(counter)
                bursts_indexes.append((counter, counter+burst_size))
                
                if burst_size > 1:
                    counter += burst_size
                    
            else:
                counter+=1
     
        return analysys(self.signal, bursts_indexes)

                    
                    
                
if __name__ == "__main__":

    wm = wave_maker()
    sig = wm.make_signal()
    
    a = wave_analyzer(sig).analyze()

    print(a)

    a.show()
    





        
        
