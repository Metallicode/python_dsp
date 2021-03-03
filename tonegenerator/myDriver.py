from tonegenerator import Tone
import time
import sounddevice as sd

f = open("notes.txt")

l = 0.1

for x in f:
    Tone(int(x), length=l, wavform="sin").generate()
    time.sleep(l)

