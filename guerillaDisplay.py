#!/usr/bin/env python
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

class guerillaDisplay(object):
    def __init__(self):
        self.options = RGBMatrixOptions()
        self.options.rows = 16
        self.options.pwm_bits = 11
        self.options.pwm_lsb_nanoseconds = 200
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
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
        self.matrix.SetPixel(x,y,self.r,self.g,self.b)

    def cellOff(self,x,y):
        self.matrix.SetPixel(x,y,0,0,0)

    def clear(self):
        self.matrix.Clear()
