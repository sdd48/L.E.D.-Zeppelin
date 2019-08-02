import numpy as np

from streamer.streamer import Streamer

class SlitherGeneratorStreamer(Streamer):
	def __init__(self, nleds, alpha=0.98, max_upper=10. ):
		super(SlitherGeneratorStreamer, self).__init__()

		self.nleds = nleds
		self.next = None
		self.lp_alpha = alpha #momentum decay
		self.max_upper = max_upper
		self.avg_power = 0.0

		self.thresh = 0.15 #toggle this to figure out what works

		self.counter = 0
		self.mask = [True]*nleds

	#data should be sound I think
	def _procInput(self, data):
		power = np.linalg.norm(data)**2 / len(data)

		upper = self.max_upper*self.avg_power
		scale = np.interp(power, [0.0, upper], [0.0, 1.0])
		self.avg_power = self.lp_alpha*self.avg_power + (1.0 - self.lp_alpha)*power

		self.mask = [scale < self.thresh] + self.mask[:-1]

		self.next = 255*np.ones((self.nleds, 3))
		if sum(self.mask) > 0:
			self.next[self.mask] = sum(self.mask)*[(0, 0, 0)]
		self.next *= scale


	def outputReady(self):
		return self.next is not None

	def output(self):
		ret = self.next
		self.next = None
		return ret