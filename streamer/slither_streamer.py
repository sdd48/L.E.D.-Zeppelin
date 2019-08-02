import numpy as np


from streamer.streamer import Streamer


class SlitherStreamer(Streamer):
	def __init__(self, nleds, min_width=1, max_width=10):
		super(SlitherStreamer, self).__init__()
		self.min_width = min_width
		self.max_width = max_width

		self.start_ind = 0
		self.counter = 0
		self.n = nleds

		self.mask = [True]*nleds


	def _procInput(self, data):
		if self.counter % self.n == 0:
			length = np.random.randint(self.min_width, self.max_width+1)
			self.mask = length*[False] + (self.n - length)*[True]
		else:
			self.mask = [True] + self.mask[:-1] #shift the lights downward

		self.next = data
		self.next[self.mask] = sum(self.mask)*[(0, 0, 0)]

		self.counter += 1

	def outputReady(self):
		return self.next is not None

	def output(self):
		ret = self.next
		self.next = None
		return ret
