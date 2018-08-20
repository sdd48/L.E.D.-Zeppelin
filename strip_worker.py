#!/usr/bin/python
import threading
import time
import queue
import numpy

from audio_functions import *
from strips.gui_strip import GuiStrip
import sound_sinks.beat_sink

#from strip.strip import Strip

exitFlag = 0

class StripWorker (threading.Thread):
    def __init__(self, swidth, fsample=44100, name="LED Strip Worker"):
        threading.Thread.__init__(self, name=name)
        self.swidth = swidth
        self.fsample = fsample
        self.name = name
        self.to_proc = queue.Queue()
        self.work = True

    def run(self):
        nleds = 150
        strip = GuiStrip(nleds)
        sink = sound_sinks.beat_sink.BeatSink(nleds, self.fsample, self.swidth)
        print("Starting " + self.name)
        a = []
        while(self.work):
            # TODO use condition var
            while self.to_proc.empty():
                time.sleep(.001)
            with self.to_proc.mutex:
                a = list(self.to_proc.queue)
                self.to_proc.queue.clear()

            for w in a:
                sink.consume(w)
                if sink.canProduce():
                    strip.setStrip(sink.produce())
                    strip.update()
        print("Exiting " + self.name)


    def stop(self):
        self.work = False


    def addWindow(self, window):
        self.to_proc.put(window)
