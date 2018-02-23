import socket
import random
import time

class Strip(object):
    def __init__(self,ip="192.168.1.188", n=150,port=5120):
        self.numleds = n
        self.port = port
        self.destip = ip
        # Array of RGB
        self.strip = bytearray(3*n)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP


    def setPixel(self, n, r, g=None, b=None):
        tup = r
        if g ==None:
            r, g, b = tup
        self.strip[3*n] = r
        self.strip[3*n+1] = g
        self.strip[3*n+2] = b


    def setAll(self, r, g=None, b=None):
        for i in range(self.numleds):
            self.setPixel(r,g,b)


    def white(self, bright=255):
        for i in range(3*self.numleds):
            self.strip[i] = 255

    def clear(self):
        self.white(0)

    def random(self):
        for i in range(3*self.numleds):
            self.strip[i] = random.randrange(255)


    def update(self):
        self.sock.sendto(self.strip, (self.destip, self.port))


    def rainbow(self, wait):
        for x in range(256):
            for i in range(self.numleds):
                #strip.setPixelColor(i, Wheel((i+j) & 255));
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
