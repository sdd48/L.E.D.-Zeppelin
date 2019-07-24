import numpy as np
from collections import deque

from streamer.streamer import Streamer


class QueueStreamer(Streamer):

  def __init__(self):
    super(QueueStreamer, self).__init__()
    self.to_update = deque()

  def input(self, data):
    self._procInput(data)

  def _procInput(self, data):
    self.to_update.append(data)

  def output(self):
    return self.to_update.popleft()

  def outputReady(self):
    return len(self.to_update) > 0
