#!usr/bin/python
import numpy as np

from sound_sinks.analysis.analysis import Analysis


class PowerAnalysis(Analysis):
	def __init__(self, numleds):
		super(PowerAnalysis, self).__init__(numleds)
		self.lp_alpha = 0.995 #momentum decay
		self.max_upper = 10.0
		self.avg_power = 0.0


	def process(self, strip, data):
		power = np.linalg.norm(data[0])**2 / len(data[0])

		upper = self.max_upper*self.avg_power
		scale = np.interp(power, [0.0, upper], [0.0, 1.0])

		self.avg_power = self.lp_alpha*self.avg_power + (1.0 - self.lp_alpha)*power

		return np.array([[int(r*scale), int(g*scale), int(b*scale)] for (r, g, b) in strip])