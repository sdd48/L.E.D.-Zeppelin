#Scott Dickson, Andrew Sikowitz
#10/13/2017
#Functions for audio processing for the lights

#from scipy.fftpack import rfft
from numpy.fft import rfft
import numpy as np

# c[0] = DC component
# c[k] with 1 <= k <= N/2 is the coefficient
# of (fs*k)/N
# bass is from 60Hz to 250Hz
# so from index 50N/fs to 250N/fs

# Returns energy of bass section in song interval
# returns [bass of fft(ar)] dot [i^(weight) for i in range(len(ar))]
#[ar] is the frequency domain represnetation of the interval
#[fs] is the  number of samples per second. The value ar[i] is the
#coefficient for [i*fs/N] hz
#[weight] is an optional weight vector such that the function returns
#[bass of fft(ar)] dot [i^(weight) for i in range(len(ar))]
def bass_of_interval(ar, fs, weight=0):
    #print(len(ar))
    c = rfft(ar)
    N = len(c)
    start = 60*N / fs
    end = 250*N / fs

    return np.linalg.norm(np.array(c[start:end]))

# Returns energy of trebble section in song interval
#Parameters as described in bass_of_interval
def treble_of_interval(ar, fs, weight=0):
    c = rfft(ar)
    N = len(c)
    start = 4000*N / fs
    end = 16000*N / fs

    return np.linalg.norm(np.array(c[start:end]))

#Best guess at max magnitude rn
norm_c = 255 / float(4.0 * 10**7)

#Given bass, treble arrays
# map them to rgb tuples in the 0-255 range
def basic_rgb(bass,treble):
    N = len(bass)
    if(len(treble) != N):
        raise ValueError

    arr = [(bass[i]*norm_c,0,treble[i]*norm_c) for i in range(N)] + np.random.normal(0,3,N)
    return map(lambda a:map(int,a),arr)

#Returns [0,1] num representing energy between frequencies sfreq and efreq
def energy_of_freq(ar, fs, sfreq, efreq):
    c = rfft(ar)
    start = sfreq * len(c) / fs
    end = efreq * len(c) / fs
    return max(np.linalg.norm(np.array(c[start:end])) * 4.0 * 10**7, 1)

def scalar_to_rainbow(i, n):
    f = i / n
    a = (1-f) / 0.2 #Blue at start
    x = np.floor(a)
    y = np.floor(255*(a-x))

    if x == 0:
        rgb = (255, y, 0)
    elif x == 1:
        rgb = (255-y, 255, 0)
    elif x == 2:
        rgb = (0, 255, y)
    elif x == 3:
        rgb = (0, 255-y, 255)
    elif x == 4:
        rgb = (y, 0, 255)
    else:
        rgb = (255, 0, 255)
    return np.array(rgb)

MIN_FREQ = 20
MAX_FREQ = 20000
def freq_per_led(ar, fs, n):
    freq_ranges = np.logspace(np.sqrt(MIN_FREQ), np.sqrt(MAX_FREQ), num=n+1, base=2) #n+1 for n intervals
    return [scalar_to_rainbow(i,n)*energy_of_freq(ar,fs,freq_ranges[i],freq_ranges[i+1]) for i in range(n)]
