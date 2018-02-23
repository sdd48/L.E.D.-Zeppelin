from strip import *
import numpy as np
s = Strip()
test = np.random.randint(0, high=255, size=(150, 3))
s.setStrip(test)
s.update()
