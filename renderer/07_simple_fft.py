import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack as fftpk
from scipy import signal as sgl
import numpy as np
from matplotlib import pyplot as plt

s_rate, signal = wavfile.read(input("filename?\n")) 

FFT = abs(scipy.fft.fft(signal))
freqs = fftpk.fftfreq(len(FFT), (1.0/s_rate))

plt.plot(freqs[range(len(FFT)//10)], FFT[range(len(FFT)//10)], color="red")

plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()
