#Scott Dickson
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
def bass_of_interval(ar, fs, weight=0):
    #print(len(ar))
    c = rfft(ar)
    N = len(c)
    start = 60*N / fs
    end = 250*N / fs
    
    return np.linalg.norm(np.array(c[start:end]))
    
# Returns energy of trebble section in song interval    
def treble_of_interval(ar, fs, weight=0):
    c = rfft(ar)
    N = len(c)
    start = 4000*N / fs
    end = 16000*N / fs
    
    return np.linalg.norm(np.array(c[start:end]))
 
#Given bass, treble arrays
# map them to rgb tuples in the 0-255 range
def basic_rgb(bass,treble):
    N = len(bass)
    if(len(treble) != N):
        raise ValueError
    
    #Best guess at max magniatude rn
    norm_c = 255 / float(4.0 * 10**7)
      
    return [(int(bass[i]*norm_c),0,int(treble[i]*norm_c)) for i in range(N)]
