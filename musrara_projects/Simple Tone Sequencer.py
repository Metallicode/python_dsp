####THIS IS THE MODULES WE NEED TO RUN OUR SCRIPT
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import datetime


####HERE ARE THE FUNCTIONS WE WILL USE TO CREATE OUR SIGNALS AND FILE
def Make_A_Tone(length, freq):
	t = np.arange(0,length, 1.0/44100)
	return list(np.sin(2*np.pi* t * freq))

def MakeFile(signal):
	now = datetime.datetime.now()
	signal *=32767
	signal = np.int16(signal)
	wavfile.write(f"file{now.strftime('%d-%m-%Y %H-%M-%S')}.wav", 44100, signal)


#####FROM HERE IS THE DRIVER CODE

#FIRST WE SET SOME VARIABLES
steps_in_sequence = 10	#HOW MENY STEPS IN OUR MELODY
signal_length = 0.1	#IN SECONDS
base_freq = 400		#IN Hz

sequence = []


#******************************************************************************#

#HERE IS THE LOOP WE USE TO SET OUR TONES
for i in range(steps_in_sequence):
	sequence += Make_A_Tone(signal_length, base_freq*i) #<----TRY PLAYING WITH THIS PART

#******************************************************************************#

sequence *= 2		#WE CAN MAKE OUR PATTERN PLAY MORE THEN ONCE...


####HERE WE CALL THE MAKEFILE FUNCTION THAT WILL SAVE OUR DATA TO A FILE
MakeFile(np.array(sequence))






