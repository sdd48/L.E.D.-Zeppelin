import aubio
import numpy as np 
import time
import collections

from streamer.streamer import Streamer
from streamer.wheel_streamer import WheelStreamer
from streamer.slither_streamer import SlitherStreamer
from streamer.slither_generator_streamer import SlitherGeneratorStreamer

class LightSnake(Streamer):
	def __init__(self, numleds):
		super(LightSnake, self).__init__()
		self.numleds = numleds
		self.wheel = WheelStreamer(numleds)
		#self.snake = SlitherStreamer(numleds, 5, 15)
		self.snake = SlitherGeneratorStreamer(numleds)

		#self.wheel.connect(self.snake)

	def input(self, data):
		#self.wheel.input(data)
		self.snake.input(data)

	def outputReady(self):
		return self.snake.outputReady()

	def output(self):
		return self.snake.output()