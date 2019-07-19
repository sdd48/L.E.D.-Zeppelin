import aubio
import numpy as np
import time
import collections

from sound_sinks.sound_sink import SoundSink
from sound_sinks.analysis.analysis import Analysis
from sound_sinks.analysis.power import PowerAnalysis
from sound_sinks.analysis.wheel_analysis import WheelAnalysis


class PowerSink(SoundSink):
	def __init__(self, numleds, fsample, frame_width):
		super(PowerSink, self).__init__(numleds, fsample, frame_width)
		self.analysis1 = WheelAnalysis(numleds, fsample, frame_width)
		self.analysis2 = PowerAnalysis(numleds, fsample, frame_width)

	#fun: nx3 array, data -> nx3 array
	def process(self, strip, data):
		result = self.analysis1.process(strip, data)
		result = self.analysis2.process(result, data)
		return result
