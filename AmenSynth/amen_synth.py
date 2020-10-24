import numpy as np
import sounddevice as sd
from scipy import signal as sgl
from scipy.io import wavfile
from itertools import cycle

class waveform:
    def __init__(self, signal, start, length):
        self.set(signal, start, length)
    def set(self, signal, start, length):
        self.s = cycle(signal[start:start+length])
    def get_next(self, buff_size):
        return np.array([next(self.s) for x in range(buff_size)])

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

samplerate, signal = wavfile.read("Amen_Break_CD.wav")
signal = np.array([x[0] for x in signal])
cutoff =6200
w = cutoff/(44100/2)

a,b = sgl.butter(4, w, 'low', analog=True)
z = sgl.filtfilt(a,b,signal)

resampled = sgl.resample(z, int(len(signal)*1.5))

tone = waveform(resampled, 0, len(resampled))

def change(e, length):
    global tone
    tone = waveform(resampled, e, length)

def play_thread(tone):
    start_idx = 0

    try:
        samplerate = 44100

        def callback(outdata, frames, time, status):
            nonlocal start_idx
            global tone
            outdata[:] = tone.get_next(len(outdata)).reshape(len(outdata),1)
            start_idx += frames

        with sd.OutputStream(channels=1, callback=callback,samplerate=samplerate):       
            print('*****press Return to quit*****')
            input()
        
    except KeyboardInterrupt:
        pass
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))


import threading

t = threading.Thread(target=play_thread, args=(tone,))
t.start()


import tkinter as tk

#create window & frames
class App:
    def __init__(self):
        self.root = tk.Tk()
        self._job = None

        w = tk.Label(self.root, text="Start")
        w.pack()
        
        self.slider = tk.Scale(self.root, from_=5, to=200000, 
                               orient="horizontal", 
                               command=self.updateValue)
        self.slider.pack()

        w2 = tk.Label(self.root, text="Length")
        w2.pack()

        self.slider2 = tk.Scale(self.root, from_=5, to=30000, 
                               orient="horizontal", 
                               command=self.updateValue)
        self.slider2.pack()

        
        self.root.mainloop()

    def updateValue(self, event):
        if self._job:
            self.root.after_cancel(self._job)
        self._job = self.root.after(500, self._do_something)

    def _do_something(self):
        self._job = None
        change(self.slider.get(), self.slider2.get())




app=App()
