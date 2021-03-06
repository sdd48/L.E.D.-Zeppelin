import socket
import random
import time
import numpy as np

class Strip(object):
    def __init__(self, n=150):
        self.numleds = n
        # Array of RGB
        self.strip = bytearray(3*n)


    def setPixel(self, n, r, g=None, b=None):
        tup = r
        if g is None:
            r, g, b = tup
        self.strip[3*n] = r
        self.strip[3*n+1] = g
        self.strip[3*n+2] = b


    # Arr is nx3
    def setStrip(self, arr):
        if isinstance(arr, np.ndarray):
            assert arr.shape == (self.numleds, 3)
            self.strip = bytearray(arr.reshape(-1).astype(np.dtype('B')))
        else:
            assert len(arr) == self.numleds
            for i,tup in enumerate(arr):
                self.setPixel(i, tuple(tup))


    def setSame(self, r, g=None, b=None):
        for i in range(self.numleds):
            self.setPixel(i, r,g,b)


    def white(self, bright=255):
        for i in range(3*self.numleds):
            self.strip[i] = 255

    def clear(self):
        self.white(0)

    def random(self):
        for i in range(3*self.numleds):
            self.strip[i] = random.randrange(255)


    def update(self):
        raise NotImplementedError("This is a base class")


    def rainbow(self, wait):
        for x in range(256):
            for i in range(self.numleds):
                self.setPixel(i, self.wheel((x+i) & 255))
            self.update()
            time.sleep(wait)


    def wheel(self, wheelpos):
        wheelpos = 255 -wheelpos
        if wheelpos < 85:
            return (255 - wheelpos*3, 0, wheelpos*3)
        elif wheelpos < 170:
            wheelpos -= 85
            return (0, wheelpos*3, 255-wheelpos*3)
        else:
            wheelpos -= 170
            return (wheelpos*3, 255-wheelpos*3, 0)
