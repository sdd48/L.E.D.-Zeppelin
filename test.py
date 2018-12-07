from strips.gui_strip import GuiStrip
from strips.led_strip import LEDStrip
import sounddevice as sd
import numpy as np

N = 300
FS = 44100


# duration = 10  # seconds
#
# #s = GuiStrip()
s = LEDStrip(N, "192.168.1.116")
#
# sd.query_devices()
#
# def print_sound(indata, outdata, frames, time, status):
#   volume_norm = np.linalg.norm(indata)
#   res = int(np.interp(volume_norm, [0, 50], [0, 255]))
#   s.setSame(res, 0, 0)
#   s.update()
#
#   # print ("|" * int(volume_norm))
#
# with sd.Stream(callback=print_sound, samplerate=FS):
#   while True:
#     test = np.random.randint(0, high=255, size=(150, 3))
#     s.setStrip(test)
#     s.update()
#     sd.sleep(100)
#

while True:
    s.rainbow(0.01)
