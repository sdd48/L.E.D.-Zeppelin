#!/usr/bin/python
import threading
import time
import queue
import numpy as np

from strips.led_strip import LEDStrip
from strips.gui_strip import GuiStrip
from streamer.toplevel.bass_power import BassPower
from streamer.toplevel.sound_meter import SoundMeter

class NewStripWorker (threading.Thread):
  def __init__(self, swidth, fsample=44100, name="New LED Strip Worker"):
    threading.Thread.__init__(self, name=name)
    self.swidth = swidth
    self.fsample = fsample
    self.name = name
    self.to_proc = queue.Queue()
    self.to_update = queue.Queue()
    self.work = True

  def run(self):
    nleds = 150
    stream = BassPower(nleds, self.fsample, self.swidth)
    #stream = SoundMeter(nleds, self.fsample, self.swidth)
    self.strip = LEDStrip(nleds)

    #Add our event timer that will update lights every period
    self.start_time = time.time()
    self.update_idx = 0
    thread = threading.Thread(target = self._updateStrip)
    thread.start()

    # Consume the new data and process it
    while(self.work):
      elem = self.to_proc.get()
      stream.input(elem)
      if stream.outputReady():
        self.to_update.put(stream.output())


  # We want to update at the same rate, without getting too behind
  def _updateStrip(self):
    ft = 0.75*self.swidth/float(self.fsample)
    while True:
      print(self.to_update.qsize())
      elem = self.to_update.get(block=True)
      self.strip.setStrip(elem)
      self.strip.update()
      time.sleep(ft)

  def stop(self):
    self.work = False


  def addWindow(self, window):
    self.to_proc.put(window)
