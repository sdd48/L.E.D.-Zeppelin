import numpy as np
from scipy import signal

from streamer.streamer import Streamer

class RunningAverageStreamer(Streamer):

  def __init__(self, alpha=0.5):
    super(RunningAverageStreamer, self).__init__()
    self.alpha = alpha
    self.prev = None
    self.res = None

  def _procInput(self, data):
    if self.prev is None:
      self.prev = np.copy(data)
      self.res = data
    else:
      self.res = (1.-self.alpha)*self.prev + self.alpha*data
      self.prev = np.copy(self.res)

  def outputReady(self):
    return self.res is not None

  def output(self):
    ret = self.res
    self.res = None
    return ret
