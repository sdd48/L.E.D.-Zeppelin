import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
from audio_functions import *
import time

from strip.strip import Strip

strip = Strip()

# song_name = "no_type.wav"

# fs,data = wavfile.read(song_name)

# a = data.T[0]

# song_length = len(a) // fs # Number of seconds in the song

# c = fft(a)
# print("fft")
# d = len(c) // 2 # because of signal symmetry
# k = np.arange(len(a[:d-1]))
# T = len(data[:d-1]) / fs
# frqLabel = k/T

# #Number of samples in 100ms
# n = int(fs / 10)

# #caluclate bass/treble for each 100ms interval
# rgbs = [freq_per_led(a[i*n:(i+1)*n], fs, strip.numleds) for i in range(song_length * 10)]

rgbs = rainbow(strip.numleds)
offset = 0
while 1:
    time.sleep(.1)
    for i in range(len(rgbs)):
        strip.setPixel((i+offset) % strip.numleds, rgbs[i][0], rgbs[i][1], rgbs[i][2])
    offset += 1
    strip.update()

#print(rgbs[0:5])

#plt.plot(range(len(rgbs)), rgbs[:,0],'r')
#plt.show()
