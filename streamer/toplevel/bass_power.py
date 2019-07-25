import aubio
import numpy as np
import time
import collections

from streamer.streamer import Streamer
from streamer.power_streamer import PowerStreamer
from streamer.queue_streamer import QueueStreamer
from streamer.wheel_streamer import WheelStreamer
from streamer.lowpass_streamer import LowPassStreamer
from streamer.gamma_streamer import GammaStreamer
from streamer.runningavg_streamer import RunningAverageStreamer

class BassPower(Streamer):
	def __init__(self, numleds, fsample, frame_width):
		super(BassPower, self).__init__()
		self.numleds = numleds
		self.lowpass = LowPassStreamer(fsample, 200., order=6)
		self.power = PowerStreamer(alpha=0.98, max_upper=3.)
		self.gamma_correct = GammaStreamer()
		self.wheel = WheelStreamer(self.numleds)
		# To prevent seizures...
		self.smooth = RunningAverageStreamer(alpha=0.8)

		self.lowpass.connect(self.power)
		self.power.connect(self.smooth)
		self.smooth.connect(self.gamma_correct)

		#self.out = QueueStreamer()
		#self.power.connect(self.out)

	def input(self, data):
		#self.power.input(data)
		self.wheel.input(data)
		self.lowpass.input(data)

	def outputReady(self):
		return self.gamma_correct.outputReady() and self.wheel.outputReady()

	def output(self):
		wheel = self.wheel.output()
		scale =  self.gamma_correct.output()
		ret = scale*wheel
		return ret.astype(int)
