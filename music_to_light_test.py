# Scott Dickson
# 10/13/2017
# Music to lights test

import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
import pickle
from audio_functions import *


song_name = "no_type.wav"
save_name = "no_type.txt"

fs,data = wavfile.read(song_name)

a = data.T[0]

song_length = len(a) / fs # Number of seconds in the song

c = fft(a)
print("Did fft")
d = len(c) / 2 # because of signal symmetry
k = np.arange(len(a[:d-1]))
T = len(data[:d-1]) / fs               
frqLabel = k/T

#Number of samples in 100ms
n = int(fs / 10)

#Record 10 values per second
bass = np.zeros(song_length * 10)
treble = np.zeros(song_length * 10)

#caluclate bass/treble for each 100ms interval 
bass = [bass_of_interval(a[i*n:(i+1)*n], fs) for i in range(song_length * 10)]
treble = [treble_of_interval(a[i*n:(i+1)*n], fs) for i in range(song_length * 10)]

RGB_tuples = basic_rgb(bass, treble)

print(RGB_tuples)

#out = open(save_name, "w")
#pickle.dump(a,out)
#out.close()

plt.plot(range(len(bass)), bass,'r')
plt.show()
