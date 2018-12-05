#!/usr/bin/python
import threading
import time
import queue
import numpy as np

from strips.led_strip import LEDStrip

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
    strip = LEDStrip(nleds)

    print("Starting " + self.name)
    a = []
    counter = 0
    r, g, b = self.randColor(strip)

    while(self.work):
      # TODO use condition var
      while self.to_proc.empty():
        time.sleep(.001)
      with self.to_proc.mutex:
        a = list(self.to_proc.queue)
        self.to_proc.queue.clear()

      thresh = 3.0
      counter += 1
      for w in a:
        power = np.linalg.norm(w)**2/len(w)
        if (power > thresh):
          r, g, b = self.randColor(strip)

        res = np.interp(power, [0, 1.5], [0, 1.0])
        up2 = (int(res*r), int(res*g), int(res*b))
        print(power)
        strip.setSame(up2)
        strip.update()
        break
      print("Exiting " + self.name)



  def randColor(self, strip):
    return strip.wheel(np.random.randint(0, 256) % 256)


  def stop(self):
    self.work = False


  def addWindow(self, window):
    self.to_proc.put(window)
