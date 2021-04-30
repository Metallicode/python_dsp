import numpy as np
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt

sample_rate = 44100

def norm(data):
    min_v = min(data)
    max_v = max(data)
    offset = min_v+max_v
    data = data+(offset/2)
    data = np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1
    return data * ((max_v/min_v)*-1)

def BIG_small(s1,s2):
    return (s2,s1) if len(s1)<len(s2) else (s1,s2)

def resample(s, n):
    return signal.resample(s, n)

def show(s_01, s_02):
    t = np.arange(0,len(s_01)/sample_rate,1.0/sample_rate)
    plt.plot(t, s_02,'orange')
    plt.plot(t, s_01,'black')
    plt.show()

def break_signal(s, t):
    step = 2**t
    return [s[i:i + step] for i in range(0, len(s), step)]

def compare_clips(clip_A, clip_B, comparison_function):
    return [comparison_function(clip_A[i], clip_B[i]) for i in range(len(clip_A))]

def max_sum(frag01, frag02):
    return 0 if sum(frag01)>sum(frag02) else 1

def evolve(signal01, signal02, dna_code):
    new_gen = []
    for i in range(len(dna_code)):
        if dna_code[i] == 0:
            new_gen.append(signal01[i])
        else:
            new_gen.append(signal02[i])

    return new_gen

def fix(l):
    new_lst = []
    for i in range(len(l)):
        for j in range(len(l[i])):
            new_lst.append(l[i][j])
    return np.array(new_lst)

def write_file(y):
    y *= 32767
    y = np.int16(y)
    wavfile.write("file.wav", 44100, y)


_, signal01 = wavfile.read("count.wav")
_, signal02 = wavfile.read("sample.wav")

signal01 = signal01
signal02 = signal02

os = BIG_small(signal01, signal02)

s1 = resample(os[1],len(os[0]))
s2 = os[0]

b1 = break_signal(s1, 6)
b2 = break_signal(s2, 6)
dna = compare_clips(b1,b2,max_sum)

child = norm(fix(evolve(b1, b2, dna)))

write_file(child)