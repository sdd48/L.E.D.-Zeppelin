import numpy as np
from scipy import signal
import aubio

from streamer.streamer import Streamer

class OnsetStreamer(Streamer):

  def __init__(self, fsample, win_size, onset_thresh=0.4, minioi_val=0.02):
    super(OnsetStreamer, self).__init__()
    self.res = None
    self.onset = aubio.onset('hfc', 2*win_size, win_size, fsample)
    self.onset.set_threshold(onset_thresh)
    self.onset.set_minioi_s(minioi_val)

  def _procInput(self, data):
    self.res = self.onset(data)

  def outputReady(self):
    return self.res is not None

  def output(self):
    ret = self.res
    self.res = None
    return ret
