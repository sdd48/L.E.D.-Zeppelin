import numpy as np
from scipy import signal

from streamer.streamer import Streamer

class LowPassStreamer(Streamer):

  def __init__(self, fsample, cutt_off, order=10):
    super(LowPassStreamer, self).__init__()
    self.fsample = fsample
    self.cutt_off = cutt_off
    cutt = cutt_off/(self.fsample / 2.0)
    self.filter = signal.butter(order, cutt, 'lowpass')
    self.zi = signal.lfilter_zi(*self.filter)
    self.res = None

  def _procInput(self, data):
    b, a = self.filter
    self.res, self.zi = signal.lfilter(b, a, data, zi=self.zi)

  def outputReady(self):
    return self.res is not None

  def output(self):
    ret = self.res
    self.res = None
    return ret
