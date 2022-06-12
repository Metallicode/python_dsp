import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

#arg 1 is length
#arg 2 is comma seperated freqs

frq = 440
sr = 44100
length = 5.0

if(len(sys.argv)>1):
	length = float(sys.argv[1])
	
if(len(sys.argv)>2):
	frq = [float(x) for x in sys.argv[2].split(",")]

t = np.arange(0, length, 1.0/sr)
s = np.zeros(int(length*sr))

for i in range(len(frq)):
	s += np.sin(2*np.pi* frq[i] *t)/len(frq)

plt.plot(t, s)
plt.show()

s *= 32767
s = np.int16(s)
print(f"rendering Complex{length}Sec.wav")
wavfile.write(f"Complex{length}Sec.wav", sr, s)

