import tkinter
import threading
import time
import numpy as np


class GuiStrip(object):
    def __init__(self, n=150, width=1200, height=480):
        self.numleds = n
        self.width = width
        self.height = height
        self.strip = bytearray(3*n)
        # Start gui thread
        self.thread = threading.Thread(target = self.runGui)
        self.thread.start()
        self.lock = threading.Lock() # This will protect the update var
        self.supdate = None # This is how we pass updates to the worker thread


    def _from_rgb(self, r, g, b):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % (r, g, b)

    def worker(self, canvas, rects):
        with self.lock:
            if self.supdate is None:
                return
            update = self.supdate
            self.supdate = None
        for i,r in enumerate(rects):
            idx = 3*i
            color = self._from_rgb(update[idx], update[idx+1], update[idx+2])
            canvas.itemconfig(r, fill=color)
        canvas.after(20, self.worker, canvas, rects)


    def runGui(self):
        root = tkinter.Tk()
        canvas = tkinter.Canvas(root, bg="black", height=self.height, width=self.width)
        rect_width = self.width // self.numleds
        rect_height = 20
        start_y = self.height//2 - rect_height//2
        end_y = self.height//2 + rect_height//2
        black = self._from_rgb(0,0,0)
        rects = []
        for i in range(self.numleds):
            start = rect_width * i
            rect = canvas.create_rectangle(start, start_y, start + rect_width, end_y, fill=black)
            rects.append(rect)

        canvas.pack()
        canvas.after(1, self.worker, canvas, rects)
        root.mainloop()


    def setPixel(self, n, r, g=None, b=None):
        tup = r
        if g ==None:
            r, g, b = tup
        self.strip[3*n] = r
        self.strip[3*n+1] = g
        self.strip[3*n+2] = b


    # Arr is nx3
    def setStrip(self, arr):
        assert len(arr) == self.numleds
        if isinstance(arr, np.ndarray):
            self.strip = bytearray(arr.reshape(-1).astype(np.dtype('B')))
        else:
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
        with self.lock:
            self.supdate = self.strip[:]


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


# This is a test
def main():
    s = GuiStrip()
    s.white()
    s.update()

if __name__ == "__main__":
    main()
