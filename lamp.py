import time
import platform

debug = True
OS = platform.system()
if OS != "Darwin":
    import board
    import neopixel


class Lamp:

    def __init__(self):
        if OS == "Darwin": return
        # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
        # NeoPixels must be connected to D10, D12, D18 or D21 to work.
        pixel_pin = board.D12

        # The number of NeoPixels
        num_pixels = 24

        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        ORDER = neopixel.GRB

        self.pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
        )

    def sunrise(self):
        if OS == "Darwin" or debug: return
        for j in range(255):
            print(j)
            self.pixels.fill((j, j, j))
            self.pixels.show()
            time.sleep(0.25)

    def sunset(self):
        if OS == "Darwin": return
        for j in range(255, 0, -1):
            print(j)
            self.pixels.fill((j, j, j))
            self.pixels.show()
            time.sleep(0.05)

    def turn_off(self):
        if OS == "Darwin": return
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
