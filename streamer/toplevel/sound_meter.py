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

class SoundMeter(Streamer):
	def __init__(self, numleds, fsample, frame_width):
		super(SoundMeter, self).__init__()
		self.numleds = numleds
		self.power = PowerStreamer(alpha=0.98, max_upper=2.)
		# To prevent seizures...
		self.smooth = RunningAverageStreamer(alpha=1.0)
		self.power.connect(self.smooth)
		self.smooth2 = RunningAverageStreamer(alpha=0.3)
		self.gamma = GammaStreamer()
		self.smooth2.connect(self.gamma)

		#self.out = QueueStreamer()
		#self.power.connect(self.out)

	def input(self, data):
		self.power.input(data)

	def outputReady(self):
		return self.smooth.outputReady()

	def output(self):
		scale =  self.smooth.output()
		num_leds = int(np.interp(scale, [0.0, 1.0], [0.0, self.numleds]))
		# Make the intesity map
		half = self.numleds // 2
		output = np.zeros((self.numleds, 3))
		output[:half,0] =  np.linspace(0, 1.0, half) # red
		output[:half,1] = 1.0 # Green
		output[half:,0] =  1.0
		output[half:,1] = np.linspace(1.0, 0, half)
		output[num_leds:,:] = 0
		self.smooth2.input(output)
		return 255*self.gamma.output()
