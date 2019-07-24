import aubio
import numpy as np
import time
import collections

from streamer.streamer import Streamer

class WheelStreamer(Streamer):
	def __init__(self, numleds):
		super(WheelStreamer, self).__init__()
		self.numleds = numleds
		self.counter = 0
		self.res = None

	def _procInput(self, data):
		self.counter += 1
		r, g, b = self.wheel(self.counter % 256)
		self.res = np.array([[r, g, b] for _ in range(self.numleds)])

	def outputReady(self):
		return self.res is not None

	def output(self):
		res = self.res
		self.res = None
		return res


	def wheel(self, wheelpos):
		wheelpos = 255 - wheelpos
		if wheelpos < 85:
			return (255 - wheelpos*3, 0, wheelpos*3)
		elif wheelpos < 170:
			wheelpos -= 85
			return (0, wheelpos*3, 255-wheelpos*3)
		else:
			wheelpos -= 170
			return (wheelpos*3, 255-wheelpos*3, 0)
