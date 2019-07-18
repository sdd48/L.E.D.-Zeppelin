import socket
import random
import time
import numpy as np
from strips import strip

class LEDStrip(strip.Strip):
    UPDATE_INTERVAL = 0.01 # 10ms
    def __init__(self, n=150, ip="192.168.1.116", port=5120):
        super(LEDStrip, self).__init__(n)
        self.port = port
        self.destip = ip
        # Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        #self.start = time.time()


    def update(self):
        self.sock.sendto(self.strip, (self.destip, self.port))
        # if time.time() > self.start + self.UPDATE_INTERVAL:
        #   self.sock.sendto(self.strip, (self.destip, self.port))
        #   self.start = time.time()
