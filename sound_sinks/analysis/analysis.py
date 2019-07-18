#!/usr/bin/python

import numpy as np


#Wrapper class, all sub classes must have a function process list[n] -> list[n]
#that performs some transformation or processing to the lights
class Analysis(object):
	def __init__(self, n, fsample, frame_width):
		self.numleds = n
		self.fsample = fsample
		self.frame_width = frame_width

	def process(self, arr, data):
		raise NotImplementedError('This is a base class')
