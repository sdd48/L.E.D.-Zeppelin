# A sound sink is given sound samples and it maps them to leds

class SoundSink(object):

    def __init__(self, numleds, fsample, frame_width):
        self.numleds = numleds
        self.fsample = fsample
        self.frame_width = frame_width


    def process(self, data):
        raise NotImplementedException("This is a base class")


    def get_blank_strip(self, numleds):
        return [[0.0, 0.0, 0.0] for _ in range(numleds)]
