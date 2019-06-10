#!/usr/bin/python

import numpy as np


#Wrapper class, all sub classes must have a function process list[n] -> list[n]
#that performs some transformation or processing to the lights
class Analysis(object):
	def __init__(self, n):
		self.numleds = n

	def process(self, arr):
		raise NotImplementedError('This is a base class')