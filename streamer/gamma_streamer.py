import numpy as np
from scipy import signal

from streamer.streamer import Streamer

class GammaStreamer(Streamer):

  def __init__(self):
    super(GammaStreamer, self).__init__()
    self.res = None

  # Reference https://github.com/Makuna/NeoPixelBus/blob/master/src/internal/NeoGamma.h
  def _procInput(self, data):
    self.res = np.power(data, 1./.45)

  def outputReady(self):
    return self.res is not None

  def output(self):
    ret = self.res
    self.res = None
    return ret
