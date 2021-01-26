from scipy.io import wavfile
import numpy as np
from datetime import datetime

def norm(data):
	min_v = min(data)
	max_v = max(data)
	offset = min_v+max_v
	data = data+(offset/2)
	data = np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1
	return data * ((max_v/min_v)*-1)

def render(beat, smpl):
	signal = []
	silence = np.zeros(len(smpl))
	for i in beat:
		if (i == "1"):
			signal+=list(np.array(smpl,dtype=np.float64))
		elif (i == "0"):
			signal+=list(silence)
		else:
			pass
			
	return np.array(signal)
	
	

SAMPLE_RATE = 44100
BPM = 200
TEMPO = 2
STEP_TIME = 60000/(BPM * TEMPO)

_, sample_a = wavfile.read("sound01.wav")
_, sample_b = wavfile.read("sound02.wav")

sample_a = sample_a[:int(SAMPLE_RATE*(STEP_TIME/1000))]
sample_b = sample_b[:int(SAMPLE_RATE*(STEP_TIME/1000))]

beat_a = "100"
beat_b = "10000"

beat_a *= len(beat_b)
beat_b *= len(beat_a)//len(beat_b)

new = norm(render(beat_a, sample_a)+render(beat_b, sample_b))


####WRITE AUDIO FILE####
now = datetime.now()
new *=32767
new = np.int16(new)
wavfile.write(f"file{now.strftime('%d-%m-%Y %H-%M-%S')}.wav", int(44100), new)
