import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

class Wavtable:
	def __init__(self, frqs=[440], length=1.0, slop_type=None, sr=44100):
		self.frqs = frqs
		self.sr = 44100
		self.length = length
		self.slop_type = slop_type
		self.t = np.arange(0, self.length, 1.0/self.sr)
		self.s = np.zeros(int(self.length*self.sr))
	
	
	def _norm(self, data):
		min_v = min(data)
		max_v = max(data)
		offset = min_v+max_v
		data = data+(offset/2)
		data = np.array([((x-min_v) / (max_v-min_v)) for x in data])*2.0-1
		return data * ((max_v/min_v)*-1)

	def _slop_maker(self, n, s_type, direction_up='false'):
		if(self.slop_type is None):
			w = [1 for i in range(n)]
		else:
			if(s_type == "lin"):
				w = np.linspace(1.0, 0, n)
			elif(s_type == "log"):
				w = 1.0/(np.logspace(0, 1.0, n))
			elif(s_type == "cir"):
				w = [1-(1-(i/(n-1)-1)**2)**0.5 for i in range(n)]
			elif(s_type == "sig"):
				w = (-np.sin(np.linspace(1.0, 0, n)*np.pi +np.pi/2)+1.0)/2.0
	
		return w if direction_up else w[::-1]
		
	def MakeSignal(self):
		slop_weights = self._slop_maker(len(self.s), s_type=self.slop_type)
		for i in range(len(self.frqs)):
			self.s += np.sin(2*np.pi* self.frqs[i] * self.t)*slop_weights[i]
		return self._norm(self.s)
	
	def Render(self, name):
		self.s *= 32767
		self.s = np.int16(self.s)
		print(f"rendering wav file..")
		wavfile.write(f"{name}.wav", self.sr, self.s)



