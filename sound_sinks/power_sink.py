import aubio
import numpy as np

from sound_sinks.sound_sink import SoundSink
from sound_sinks.analysis.analysis import Analysis
from sound_sinks.analysis.power import PowerAnalysis
from sound_sinks.analysis.wheel_analysis import WheelAnalysis


class PowerSink(SoundSink):
	def __init__(self, numleds, fsample, frame_width, window_size=1024):
		super(PowerSink, self).__init__(numleds, fsample, frame_width)

		self.strip_state = super(PowerSink, self).get_blank_strip(numleds)

		self.analysis1 = WheelAnalysis(numleds, fsample, frame_width)
		self.analysis2 = PowerAnalysis(numleds, fsample, frame_width)

	#fun: nx3 array, data -> nx3 array
	def consume(self, strip, data):
		result = self.analysis1.process(strip, data)
		result = self.analysis2.process(result, data)
		self.strip_state = result

	def produce(self):
		return self.strip_state


	def canProduce(self):
		return True
