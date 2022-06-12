import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

#first arg is length
## 2nd arg is frq

frq = 440
sr = 44100
length = 5.0

if(len(sys.argv)>1):
	length = int(sys.argv[1])
	
if(len(sys.argv)>2):
	frq = float(sys.argv[2])

t = np.arange(0, length, 1.0/sr)
s = np.sin(2*np.pi* frq *t)

s *= 32767
s = np.int16(s)
print(f"rendering {frq}Hz_{length}Sec.wav")
wavfile.write(f"{frq}Hz_{length}Sec.wav", sr, s)


