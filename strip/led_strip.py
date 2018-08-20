import socket
import random
import time
import numpy as np
import strip

class LEDStrip(strip.Strip):
    def __init__(self, n=150, ip="192.168.1.188", port=5120):
        super(LEDStrip, self).__init__(n)
        self.port = port
        self.destip = ip
        # Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP


    def update(self):
        self.sock.sendto(self.strip, (self.destip, self.port))
