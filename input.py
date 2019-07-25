import pyaudio
import wave
import time
import sys
import strip_worker
import sounddevice as sd
import numpy as np
from scipy import signal

SAMPLES_PER_WINDOW = 1024
FS = 44100
device=6

# How much latency to update the lightstrip
latency_comp = 0.02
frame_counter = round(latency_comp*FS/SAMPLES_PER_WINDOW)
#output_device
# Create strip thread
#worker = strip_worker.StripWorker(SAMPLES_PER_WINDOW, FS, "Light Strip Worker")
worker = strip_worker.NewStripWorker(SAMPLES_PER_WINDOW, FS, "New Light Strip Worker")

worker.start()

print(sd.query_devices())
print(sd.query_devices(device, 'input'))


def input_sound(indata, outdata, frames, sd_time, status):
  global frame_counter
  if frame_counter == 0:
    outdata[:,:2] = indata[:,:2]
  else:
    frame_counter -= 1
  #print(sd_time.inputBufferAdcTime)
  worker.addWindow(indata[:,0].flatten())

def output_sound(outdata, frames, time, status):
  pass

with sd.Stream(callback=input_sound, samplerate=FS, device=device, blocksize=SAMPLES_PER_WINDOW, latency='low'):
  while True:
    sd.sleep(100)


# stop thread
worker.stop()
worker.join()
