import aubio
import numpy as np
import time
import collections

from streamer.streamer import Streamer
from streamer.onset_streamer import OnsetStreamer

class OnsetStrobe(Streamer):
	def __init__(self, numleds, fsample, frame_width):
		super(OnsetStrobe, self).__init__()
		self.numleds = numleds
		self.onset = OnsetStreamer(fsample, frame_width)

	def input(self, data):
		self.onset.input(data)


	def outputReady(self):
		return self.onset.outputReady()

	def output(self):
		val = self.onset.output()
		if val > 0.5:
			return 255*np.ones((self.numleds, 3))
		else:
			return np.zeros((self.numleds, 3))
