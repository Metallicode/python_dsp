import numpy as np
from scipy.io import wavfile
import glob
from datetime import datetime

def norm(data):
    min_v = min(data)
    max_v = max(data)
    offset = min_v+max_v
    data = data+(offset/2)
    data = np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1
    return data * ((max_v/min_v)*-1)


#set sample pack & loop string 
pack = "pack01"
loop_string = "07704050405050201063225412457643100"*10
speed = 5000
pitch = 0.5



#read all files in folder pack
all_files_in_dir = glob.glob(f"{pack}/*.wav")

sample_pool = []

for i in range(len(all_files_in_dir)):
    _, signal = wavfile.read(all_files_in_dir[i])
    sample_pool.append(np.array(signal,dtype=np.float64)[:speed])





#Build Loop
new = []

for x in range(len(loop_string)):
    current = int(loop_string[x])
    current_sample_length = len(sample_pool[current])
    
    l = list(sample_pool[current])   
    if x%4==0:
        l = l[:current_sample_length//2]*2    
    elif x%6==0:
        l = l[:current_sample_length//3]*3
    elif x%5==0:
        l = l[::-1]
   
    new += l

new = norm(new)







####WRITE AUDIO FILE####
now = datetime.now()
new *=32767
new = np.int16(new)
wavfile.write(f"exports/file{now.strftime('%d-%m-%Y %H-%M-%S')}.wav", int(44100*pitch), new)
