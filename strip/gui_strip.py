import tkinter
import threading
import time
import numpy as np
import strip


class GuiStrip(strip.Strip):
    def __init__(self, n=150, width=1200, height=480):
        super(GuiStrip, self).__init__(n)
        self.width = width
        self.height = height
        # Start gui thread
        self.lock = threading.Lock() # This will protect the update var
        self.supdate = None # This is how we pass updates to the worker thread
        self.thread = threading.Thread(target = self.runGui)
        self.thread.start()


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


    def update(self):
        with self.lock:
            self.supdate = self.strip[:]
