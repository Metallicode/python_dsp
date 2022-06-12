import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

#first arg is length
#2nd arg is base freq
#3rd arg is brainwave type

sr = 44100
brainwaves = {"delta":2, "theta":5, "alpha":10, "beta":20, "gamma":50}

length = int(sys.argv[1])
frq = float(sys.argv[2])
diff = brainwaves[sys.argv[3].lower()]

t = np.arange(0, length, 1.0/sr)

s=np.vstack((np.sin(2*np.pi* frq *t), np.sin(2*np.pi* (frq+diff) *t)))
s=s.transpose()

s *= 32767
s = np.int16(s)
print(f"rendering {sys.argv[3].lower()}_Binural_{frq}Hz_{length}Sec.wav")
wavfile.write(f"{sys.argv[3].lower()}_Binural_{frq}Hz_{length}Sec.wav", sr, s)


