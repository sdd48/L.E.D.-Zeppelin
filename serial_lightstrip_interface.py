# Scott Dickson
# Aaaron Wisner
#9/22/2017

# 0x00 is the escape byte
# 0x00 followed by 0xFF signals the start of the array to send to the lights
#s l i p with a checksum at the end i.e. last byte should be the XOR
# of all the previous elements.  Arduino should check this to confirm valid data

import serial

class LightStrip(Object):
    def __init__(self, b, n, port):
        self.baud_rate = b
        self.numer_of_leds = n # Number of LEDs on the strip
        self.light_values = [(0,0,0)]*n # Array for each light's RGB 
        self.port = port # String of serial port to send data
        
    #Set RGB value of LED n.
    #If update: Send configuration over serial
    def set_led(n, r = 0, g = 0, b = 0, update = True):
        self.light_values[n-1] = (r, g, b)
    
    #Set all LEDs to a uniform intensity
    #If update: Send configuration over serial
    def set_all(r = 0, g = 0, b = 0, updat = True):
        self.light_values = [(r, g, b) for x in self.light_values]
        
        
    #Send array of RGB values by serial    
    def send():
        #SEND
        ser = serial.Serial(p, b, timeout = 1)
        ser.baudrate = b
        ser.write(prepare_list())
        ser.close()
        return 0
    
    # Prepare the class' list for SLIP transmit
    def prepare_list():
        
        packet = self.light_values.insert(0, (0xFF, 0xFF, 0xFF)).insert(0, (0x03,0x05, 0x07))
        # Verification 
        xor = 0x00
        for e in packey:
            xor = xor ^ e[0] ^e[1] ^ e[2]
        
        packet = self.light_values.extend([(xor, xor, xor)])
        
        return packet
        
            
        
