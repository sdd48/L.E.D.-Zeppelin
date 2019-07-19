#!/usr/bin/python
import threading
import time
import queue
import numpy as np

from strips.led_strip import LEDStrip
from strips.gui_strip import GuiStrip
from sound_sinks.power_sink import PowerSink

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
    nleds = 300
    lp_alpha = 0.995
    max_upper = 10.0 # Twice the average power

    avg_pow = 0.0
    strip = GuiStrip(nleds)

    print("Starting " + self.name)
    a = []
    counter = 0
    while(self.work):
      # TODO use condition var
      while self.to_proc.empty():
        time.sleep(.001)
      with self.to_proc.mutex:
        a = list(self.to_proc.queue)
        self.to_proc.queue.clear()

      counter += 1
      power = np.linalg.norm(a[0])**2/len(a[0])
      #print(power)
      # crude low pass
      r,g,b = strip.wheel(counter % 256)
      upper = max_upper*avg_pow
      res = np.interp(power, [0, upper], [0, 1.0])
      avg_pow = lp_alpha*avg_pow + (1.0-lp_alpha)*power
      print(power, avg_pow)
      up2 = (int(res*r), int(res*g), int(res*b))
      strip.setSame(up2)

      strip.update()

    print("Exiting " + self.name)


  def stop(self):
    self.work = False


  def addWindow(self, window):
    self.to_proc.put(window)



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
    nleds = 300
    sink = PowerSink(nleds, self.fsample, self.swidth)

    self.strip = LEDStrip(nleds)

    print("Starting " + self.name)
    a = []

    #Add our event timer that will update lights every period
    self.start_time = time.time()
    self.update_idx = 0
    self._updateStrip()

    # Consume the new data and process it
    while(self.work):
      elem = self.to_proc.get()
      update = sink.process(self.strip, elem)
      self.to_update.put(update)

    print("Exiting " + self.name)


  def _updateStrip(self):
    try:
      elem = self.to_update.get(block=False)
      self.strip.setStrip(elem)
      self.strip.update()
    except queue.Empty:
      pass
    finally:
      self.update_idx += 1
      ft = 0.99*self.swidth/float(self.fsample)
      next = self.start_time + self.update_idx*ft
      threading.Timer(next - time.time(), self._updateStrip).start()


  def stop(self):
    self.work = False


  def addWindow(self, window):
    self.to_proc.put(window)
