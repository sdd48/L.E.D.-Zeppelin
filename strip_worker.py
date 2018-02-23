#!/usr/bin/python
import threading
import time
import Queue
import numpy

exitFlag = 0

class StripWorker (threading.Thread):
    def __init__(self, name="LED Strip Worker", fsample=44100):
        threading.Thread.__init__(self, name=name)
        self.fsample = fsample
        self.name = name
        self.to_proc = Queue.Queue()
        self.work = True


    def run(self):
        print "Starting " + self.name

        while(self.work):
            frame = self.to_proc.get(block=True, timeout=None) #block until work
            # Queue contains a bunch of wave.readframes
            # TODO control lights

        print "Exiting " + self.name


    def stop(self):
        self.work = False


    def addFrame(self, frame):
        self.to_proc.put(frame)
