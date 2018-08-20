# A sound sink is given sound samples and it maps them to leds
import aubio
import numpy as np
from sound_sinks.sound_sink import SoundSink

class BeatSink(SoundSink):

    def __init__(self, numleds, fsample, frame_width, window_size=1024):
        super(BeatSink, self).__init__(fsample, numleds, frame_width)
        self.tempo = aubio.tempo("default", window_size, frame_width, fsample)
        # self.window_size = window_size
        self.frame = np.zeros(frame_width, dtype=np.float32)
        self.beats = np.zeros((self.numleds, 3))


    def consume(self, data):
        subs = data[0,:].astype(np.float32)
        beat = self.tempo(subs)
        if beat:
            self.beats = 255*np.ones((self.numleds, 3))
        else:
            self.beats /= 1.5

    def canProduce(self):
        return True


    def produce(self):
        return self.beats
