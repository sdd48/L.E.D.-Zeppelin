from strips.gui_strip import GuiStrip
from strips.led_strip import LEDStrip
import numpy as np

#s = gui_strip.LEDStrip()
s = GuiStrip()
test = np.random.randint(0, high=255, size=(150, 3))
s.setStrip(test)
s.update()

while True:
    s.rainbow(0.01)
