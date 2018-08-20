#import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
from audio_functions import *
import time

from strip.strip import Strip

strip = Strip()


rgbs = rainbow(strip.numleds)
counter = 0
stage = 1
while 1:
    time.sleep(.04)
    strip.setSame(counter % 255, 0,255 - (counter % 255))
    counter += stage
    if counter % 255 == 0:
    	time.sleep(.1)
    	stage = stage * -1
    strip.update()

#plt.plot(range(len(rgbs)), rgbs[:,0],'r')
#plt.show()
