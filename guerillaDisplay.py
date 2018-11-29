#!/usr/bin/env python
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class guerillaDisplay(object):
    def __init__(self):
        self.options = RGBMatrixOptions()
        self.options.rows = 16
        self.options.chain_length = 1
        self.options.parallel = 1
        self.options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'
        self.font = graphics.Font()
        self.font.LoadFont("rpi-rgb-led-matrix/fonts/5x8.bdf")
        self.textColor = graphics.Color(255, 0, 0)
    def initiate(self):
        self.matrix = RGBMatrix(options = self.options)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()

    def set(self, m):
        self.msg = m

    def cellOn(self,x,y,r,g,b):
        pos = 3 #align left
        #self.msg = "."
        self.matrix.SetPixel(x,y,r,g,b)
        #graphics.DrawText(self.offscreen_canvas, self.font, pos, 10, self.textColor, self.msg)
        #self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

    def cellOff(self,x,y):
        self.matrix.SetPixel(x,y,0,0,0)

    def clear(self):
        self.matrix.Clear()
