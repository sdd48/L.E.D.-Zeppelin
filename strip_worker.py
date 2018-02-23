#!/usr/bin/python
import threading
import time
import queue
import numpy

from audio_functions import *
from strip.strip import Strip
strip = Strip()

exitFlag = 0

class StripWorker (threading.Thread):
    def __init__(self, name="LED Strip Worker", fsample=44100):
        threading.Thread.__init__(self, name=name)
        self.fsample = fsample
        self.name = name
        self.to_proc = queue.Queue()
        self.work = True

    def run(self):
        print("Starting " + self.name)
        a = []
        while(self.work):
            while self.to_proc.empty():
                time.sleep(.1)
            with self.to_proc.mutex:
                a = list(self.to_proc.queue)
                self.to_proc.queue.clear()
            rgb = freq_per_led(a[0], self.fsample, strip.numleds) #a[0] is first channel
            strip.setStrip(rgb)
            strip.update()

        print("Exiting " + self.name)


    def stop(self):
        self.work = False


    def addFrame(self, frame):
        self.to_proc.put(frame)
