# A sound sink is given sound samples and it maps them to leds

class SoundSink(object):

    def __init__(self, numleds, fsample, frame_width):
        self.numleds = numleds
        self.fsample = fsample
        self.frame_width = frame_width


    def consume(self, data):
        raise NotImplementedException("This is a base class")

    def canProduce(self):
        return False


    def produce(self):
        #return [(0, 0, 0) for i in range(self.numleds)]
        raise NotImplementedException("This is a base class")


        #analysis, power, low pass, fft, sound sinks use analyses
