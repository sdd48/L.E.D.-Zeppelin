import numpy as np

class Streamer(object):

  def __init__(self):
    self._next = []

  def input(self, data):
    self._procInput(data)
    # We infer a connection if there is a successor
    if len(self._next) > 0:
      while self.outputReady():
        out = self.output()
        for n in self._next:
          n.input(out)

  def connect(self, next):
    self._next.append(next)

  def _procInput(self, data):
    raise NotImplementedException("This is a base class")

  def outputReady(self):
    return False

  def output(self):
    raise NotImplementedException("This is a base class")
