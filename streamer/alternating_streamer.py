import aubio
import numpy as np
import time
import collections

from streamer.streamer import Streamer

class AlternatingStreamer(Streamer):
	def __init__(self, nleds, width=1):
		super(AlternatingStreamer, self).__init__()
		self.state = 0 #0 to zero out evens, 1 to zero out odds
		self.next = None

		whole_chunks = int(nleds / width)
		rem = nleds % width
		even_split = whole_chunks % 2 == 0


		self.flip_arr = ([True]*width+[False]*width)*int(whole_chunks / 2)
		if not even_split:
			self.flip_arr += [True]*width
		self.flip_arr += [even_split]*rem

	#data should be a light strip, Nx3
	def _procInput(self, data):
		data[self.flip_arr] = [[0,0,0]]*sum(self.flip_arr)

		self.flip_arr = [not e for e in self.flip_arr]
		
		self.next = data


	def outputReady(self):
		return self.next is not None

	def output(self):
		ret = self.next
		self.next = None

		return ret
