import aubio
import numpy as np
import time
import collections

from streamer.streamer import Streamer

class AlternatingStreamer(Streamer):
	def __init__(self):
		super(AlternatingStreamer, self).__init__()
		self.state = 0 #0 to zero out evens, 1 to zero out odds
		self.next = None

	#data should be a light strip, Nx3
	def _procInput(self, data):
		data[self.state::2] = [[0,0,0]]*len(data[self.state::2])
		self.state = int(not self.state)
		self.next = data


	def outputReady(self):
		return self.next is not None

	def output(self):
		ret = self.next
		self.next = None

		return ret
