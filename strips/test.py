from strips import gui_strip
from strips import led_strip
import numpy as np

#s = gui_strip.LEDStrip()
s = gui_strip.GuiStrip()
test = np.random.randint(0, high=255, size=(150, 3))
s.setStrip(test)
s.update()

while True:
    s.rainbow(0.01)
