import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.fftpack as fftpk
import scipy

def norm(data):
    min_v = min(data)
    max_v = max(data)
    return np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1
    
def slop(n, s_type = "lin", direction_up='false'):
	if(s_type == "lin"):
		w = np.linspace(1.0, 0, n)
	elif(s_type == "log"):
		w = 1.0/(np.logspace(0, 1.0, n))
	elif(s_type == "cir"):
		w = [1-(1-(i/(n-1)-1)**2)**0.5 for i in range(n)]
	elif(s_type == "sig"):
		w = (-np.sin(np.linspace(1.0, 0, n)*np.pi +np.pi/2)+1.0)/2.0

	return w if direction_up else w[::-1]



sr = 44100
length = 0.1
n_overtones = 20
fondemental = 100
weights = slop(n_overtones, s_type = "cir")

plt.bar(range(n_overtones), weights)
plt.show()



t = np.arange(0, length, 1.0/sr)

signal = np.zeros(int(sr*length))
series = []
for i in range(1,n_overtones,1):
	signal += np.sin(2*np.pi*(fondemental*i)*t)*weights[i]
	#series += list(np.sin(2*np.pi*(fondemental*i)*t))
	
signal = norm(signal)

FFT = abs(scipy.fft.fft(signal))
freqs = fftpk.fftfreq(len(FFT), (1.0/sr))

plt.plot(freqs[range(len(FFT)//n_overtones)], FFT[range(len(FFT)//n_overtones)])  
plt.show()




#plt.plot(t, signal)
#plt.show()

#signal = norm(series)


#signal *= 32767
#signal = np.int16(signal)
#wavfile.write("file7.wav", sr, signal)


