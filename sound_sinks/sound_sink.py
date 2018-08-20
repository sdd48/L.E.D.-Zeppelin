# A sound sink is given sound samples and it maps them to leds

class SoundSink(object):

    def __init__(self, fsample, numleds, frame_width):
        self.numleds = numleds
        self.fsample = fsample
        self.frame_width = frame_width


    def consume(self, data):
        pass

    def canProduce(self):
        return False


    def produce(self):
        return [(0, 0, 0) for i in range(self.numleds)]
