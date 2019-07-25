import aubio
import numpy as np
import time
import collections

from streamer.streamer import Streamer

class PowerStreamer(Streamer):
	def __init__(self, alpha=0.98, max_upper=10.):
		super(PowerStreamer, self).__init__()
		self.lp_alpha = alpha #momentum decay
		self.max_upper = max_upper
		self.avg_power = 0.0
		self.next = None

	def _procInput(self, data):
		power = np.linalg.norm(data)**2 / len(data)
		upper = self.max_upper*self.avg_power
		scale = np.interp(power, [0.0, upper], [0.0, 1.0])
		self.avg_power = self.lp_alpha*self.avg_power + (1.0 - self.lp_alpha)*power
		self.next = scale

	def outputReady(self):
		return self.next is not None


	def output(self):
		ret = self.next
		self.next = None
		return ret
