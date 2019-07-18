import numpy as np

from sound_sinks.analysis.analysis import Analysis

class WheelAnalysis(Analysis):
	def __init__(self, numleds):
		super(WheelAnalysis, self).__init__(numleds)
		self.counter = 0

	def process(self, strip, data):
		self.counter += 1

		r, g, b = self.wheel(self.counter % 256)

		return np.array([[r, g, b] for _ in range(self.numleds)])



	def wheel(self, wheelpos):
		wheelpos = 255 - wheelpos
		
		if wheelpos < 85:
			return (255 - wheelpos*3, 0, wheelpos*3)
		elif wheelpos < 170:
			wheelpos -= 85
			return (0, wheelpos*3, 255-wheelpos*3)
		else:
			wheelpos -= 170
			return (wheelpos*3, 255-wheelpos*3, 0)
