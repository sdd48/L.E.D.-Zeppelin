import aubio
import numpy as np
import time
import collections

from streamer.streamer import Streamer
from streamer.onset_streamer import OnsetStreamer
from streamer.wheel_streamer import WheelStreamer

class OnsetStrobe(Streamer):
	def __init__(self, numleds, fsample, frame_width):
		super(OnsetStrobe, self).__init__()
		self.numleds = numleds
		self.onset = OnsetStreamer(fsample, frame_width)
		self.wheel = WheelStreamer(numleds)

	def input(self, data):
		self.wheel.input(data)
		self.onset.input(data)


	def outputReady(self):
		return self.onset.outputReady() and self.wheel.outputReady()

	def output(self):
		val = self.onset.output()
		strip = self.wheel.output()

		if val > 0.5:
			return strip
		else:
			return np.zeros((self.numleds, 3))
