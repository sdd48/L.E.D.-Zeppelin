import pyaudio
import wave
import time
import sys
import strip_worker
import sounddevice as sd
import numpy as np

SAMPLES_PER_WINDOW = 2048
FS = 44100
device=0
# Create strip thread
worker = strip_worker.StripWorker(SAMPLES_PER_WINDOW, FS, "Light Strip Worker")
worker.start()

print(sd.query_devices())
print(sd.query_devices(0, 'input'))

def print_sound(indata, outdata, frames, time, status):
  print("Got data")
  for w in indata:
    worker.addWindow(indata)
  # print ("|" * int(volume_norm))

with sd.Stream(device=device, callback=print_sound, samplerate=FS, blocksize=SAMPLES_PER_WINDOW):
  while True:
    sd.sleep(100)


# stop thread
worker.stop()
worker.join()
