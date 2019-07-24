import aubio
import numpy as np
import time
import collections

from streamer.streamer import Streamer
from streamer.power_streamer import PowerStreamer
from streamer.queue_streamer import QueueStreamer
from streamer.wheel_streamer import WheelStreamer

class TopStreamer(Streamer):
	def __init__(self, numleds, fsample, frame_width):
		super(TopStreamer, self).__init__()
		self.numleds = numleds
		self.power = PowerStreamer()
		self.wheel = WheelStreamer(self.numleds)
		self.out = QueueStreamer()
		self.power.connect(self.out)

	def input(self, data):
		self.power.input(data)
		self.wheel.input(data)

	def outputReady(self):
		return self.out.outputReady() and self.wheel.outputReady()

	def output(self):
		wheel = self.wheel.output()
		scale =  self.out.output()
		ret = scale*wheel
		return ret.astype(int)
