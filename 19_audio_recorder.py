import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io import wavfile

sr = 48000
time = 5

signal = sd.rec(int(time*sr),  samplerate=sr, channels=1)
sd.wait()

sd.play(signal)

#draw
plt.plot(range(len(signal)), signal, "black")
plt.show()

#write file
signal*= 32767
signal = np.int16(signal)
wavfile.write("file.wav", sr, signal)
