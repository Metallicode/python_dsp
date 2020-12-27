import numpy as np
from scipy.io import wavfile
import glob
from datetime import datetime
import random


def norm(data):
	min_v = min(data)
	max_v = max(data)
	offset = min_v+max_v
	data = data+(offset/2)
	data = np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1
	return data * ((max_v/min_v)*-1)



loop_string = input("enter loop string:\n")


speed = 8000
pack = "pack"+input("pack number:\n")

all_files_in_dir = glob.glob(f"{pack}/*.wav")


sample_pool = []

for i in range(len(all_files_in_dir)):
	_, signal = wavfile.read(all_files_in_dir[i])
	sample_pool.append(np.array(signal,dtype=np.float64)[:speed])


loop = []

for i in range(len(loop_string)):
	current = loop_string[i]
	inx = ord(current)%len(all_files_in_dir)
	current_sample_length = len(sample_pool[inx])
    
	l = list(sample_pool[inx])
	if i%3==0:
		v = random.choice([2,4,8,16,32,64])
		l = l[:current_sample_length//v]*v    
	elif i%4==0:
		l = l[:current_sample_length//3]*3
	elif i%5==0:
		l = l[::-1]
	loop += l




loop *= 2

loop = norm(loop)
now = datetime.now()
loop *=32767
loop = np.int16(loop)
wavfile.write(f"file{now.strftime('%d-%m-%Y %H-%M-%S')}.wav",44100, loop)
