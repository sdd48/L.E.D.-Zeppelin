import pyaudio
import wave
import time
import sys
import strip_worker
import sounddevice as sd
import numpy as np

SAMPLES_PER_WINDOW = 1024
FS = 44100
device=4
# Create strip thread
#worker = strip_worker.StripWorker(SAMPLES_PER_WINDOW, FS, "Light Strip Worker")
worker = strip_worker.NewStripWorker(SAMPLES_PER_WINDOW, FS, "New Light Strip Worker")

worker.start()

print(sd.query_devices())
print(sd.query_devices(device, 'input'))

def print_sound(indata, frames, time, status):
  worker.addWindow(indata.flatten())


with sd.InputStream(callback=print_sound, samplerate=FS, blocksize=SAMPLES_PER_WINDOW, latency='low', channels=1):
  while True:
    sd.sleep(100)


# stop thread
worker.stop()
worker.join()
