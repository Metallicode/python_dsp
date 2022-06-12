import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

#arg 1 is length
#arg 2 is freq
#arg 3 is osc_n
#arg 4 is q

frq = 440
sr = 44100
length = 5.0
osc_n = 2
q = 1


if(len(sys.argv)>1):
	length = float(sys.argv[1])
	
if(len(sys.argv)>2):
	frq = float(sys.argv[2])
	
if(len(sys.argv)>3):
	osc_n = int(sys.argv[3])
	
if(len(sys.argv)>4):
	q = float(sys.argv[4])

t = np.arange(0, length, 1.0/sr)

s = np.sin(2*np.pi*frq*t)/osc_n

for i in range(osc_n-1):
	s += np.sin(2*np.pi* (frq+(i*(q/osc_n))) *t)/osc_n

plt.plot(t, s)
plt.show()

s *= 32767
s = np.int16(s)
print(f"rendering cluster{length}Sec.wav")
wavfile.write(f"cluster_{length}Sec.wav", sr, s)

