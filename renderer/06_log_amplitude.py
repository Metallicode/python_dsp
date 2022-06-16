import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def norm(data):
	min_v = min(data)
	max_v = max(data)
	offset = min_v+max_v
	data = data+(offset/2)
	data = np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1
	return data * ((max_v/min_v)*-1)


#arg 1 is length
#arg 2 is fondamental 
#arg 3 is n_overtons 

frq = 100
sr = 44100
length = 5.0
n_overtons = 5

if(len(sys.argv)>1):
	length = float(sys.argv[1])
	
if(len(sys.argv)>2):
	frq = float(sys.argv[2])
	
if(len(sys.argv)>3):
	n_overtons = int(sys.argv[3])


t = np.arange(0, length, 1.0/sr)
s = np.zeros(int(length*sr))

for i in range(n_overtons):
	s += np.sin(2*np.pi* (frq*(i+1)) *t)*(1/(i+1))

s=norm(s)

plt.bar(range(n_overtons),[1/(x+1) for x in range(n_overtons)])
plt.show()
plt.plot(t, s)
plt.show()

s *= 32767
s = np.int16(s)
print(f"rendering StringHarmony{length}Sec_LogGain.wav")
wavfile.write(f"StringHarmony{length}Sec_LogGain.wav", sr, s)



