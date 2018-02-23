import socket


class Strip(object):
    def __init__(self,ip="192.168.1.188", n=150,port=5120):
        self.numleds = n
        self.port = port
        self.destip = ip
        # Array of RGB
        self.strip = bytearray(3*n)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP


    def setPixel(self, n, r, g, b):
        self.strip[3*n] = r
        self.strip[3*n+1] = g
        self.strip[3*n+2] = b


    def white(self, bright=255):
        for i in range(3*self.numleds):
            self.strip[i] = 255


    def update(self):
        self.sock.sendto(self.strip, (self.destip, self.port))
