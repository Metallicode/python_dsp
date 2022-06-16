import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack as fftpk
from scipy import signal as sgl
import numpy as np
from wavetables import Wavtable

class PhysicalSynth:
	def __init__(self):
		self.sample_rate = None
		self.file_name = "tone"
		self.length = 0
		self.raw_data = None
		self.signal = None
		self.lp_cutoff_freq = 700
		self.hp_cutoff_freq = 100
		self.FFT = None
		self.freqs = None
		self.peaks = None
		self.min_peak_heigth = 50
		self.freq_list = None
		self.slop_type = None
		self.wavtable = None
		self.generated_signal = None

	def _read_file(self):
		self.sample_rate, self.raw_data = wavfile.read(self.file_name)
		
	def _marge_to_mono(self):
		if(len(np.shape(self.raw_data))>1):
			self.raw_data = self.raw_data[:, 0] + self.raw_data[:, 1]

	def _norm(self, data):
		min_v = min(data)
		max_v = max(data)
		offset = min_v+max_v
		data = data+(offset/2)
		return np.array([((x-min_v) / (max_v-min_v)) for x in data], dtype='float')*2.0-1

	def _filter(self):
		w = self.lp_cutoff_freq/(self.sample_rate/2)
		a,b = sgl.butter(4, w, "low", analog=False)
		self.signal = sgl.filtfilt(a,b,self.signal)
		
		w = self.hp_cutoff_freq/(self.sample_rate/2)
		a,b = sgl.butter(4, w, "high", analog=False)
		self.signal = sgl.filtfilt(a,b,self.signal)
			
	def _do_fft(self):
		self.FFT = abs(scipy.fft.fft(self.signal))
		self.freqs = fftpk.fftfreq(len(self.FFT), (1.0/self.sample_rate))
	
	def _read_peaks(self):      
		indices = sgl.find_peaks(self.FFT[range(len(self.FFT)//20)], height=self.min_peak_heigth, width=2)[0]
		peaks = [self.freqs[x] for x in indices]
		self.freq_list = [np.roll(i, int(i%180)) for i in peaks]
		
	def _generate_wavetable(self):
		self.wavtable = Wavtable(self.freq_list, self.length, self.slop_type, self.sample_rate)
		self.generated_signal = self._norm(self.wavtable.MakeSignal())
	
	def _make_file(self):
		self.generated_signal *= 32767
		self.generated_signal = np.int16(self.generated_signal)
		print(f"rendering wav file..")
		wavfile.write(f"x_{self.file_name.split('/')[1]}", self.sample_rate, self.generated_signal)
		
		
	def Load(self):
		self._read_file()
		
	def Prepare(self):
		self._marge_to_mono()
		self.signal = self._norm(self.raw_data)	
		
	def Analyze(self):
		self._filter()
		self._do_fft()
		self._read_peaks()	
		
	def Set(self,fileName=None,length=None,slop_type=None,lp_cutoff_freq=None,
hp_cutoff_freq=None,min_peak_heigth=None):
		if (fileName is not None):
			self.file_name=fileName
		if (length is not None):
			self.length=length
		if (slop_type is not None):
			self.slop_type=slop_type		
		if (lp_cutoff_freq is not None):
			self.lp_cutoff_freq=lp_cutoff_freq
		if (hp_cutoff_freq is not None):
			self.hp_cutoff_freq=hp_cutoff_freq
		if (min_peak_heigth is not None):
			self.min_peak_heigth=min_peak_heigth					
		
	def Synthesize(self, fn, fl = 1.0, st = "log"):
		self.Set(fileName=fn, length=fl, slop_type=st)		
		self.Load()
		self.Prepare()
		self.Analyze()
		
		self._generate_wavetable()
		self._make_file()

if __name__ == "__main__":
	p = PhysicalSynth()
	x = input('filename\n')
	p.Synthesize(fn=f"woodz/{x}.wav")



	

