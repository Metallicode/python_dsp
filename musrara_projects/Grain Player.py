import time
from scipy.io import wavfile
import numpy as np

def OpenFile(name):
	samplerate, signal = wavfile.read(f"{name}")
	return np.array(signal,dtype=np.float64)


def MakeFile(signal):
	signal *=32767
	signal = np.int16(signal)
	wavfile.write(f"file.wav", 44100, signal)

def norm(data):
	min_v = min(data)
	max_v = max(data)
	offset = min_v+max_v
	data = data+(offset/2)
	data = np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1
	return data * ((max_v/min_v)*-1)


signal = OpenFile("grain_player.wav")

segments = 100
grain_size = 3
directionIsUp = True
buff = len(signal)//segments


x = 0
z = 5
ls = []

while z > 0:

	ls += list(signal[x:x+(buff*grain_size)])
	if directionIsUp is True:
		x+=buff
	else:
		x-=buff
		
	if x > segments*buff:
		directionIsUp = False
	elif x < 0: 
		directionIsUp = True
		z -=1

MakeFile(norm(ls))


