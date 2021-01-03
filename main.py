import feedparser
import os
import requests
import time
import platform
import datetime

OS = platform.system()

if OS != "Darwin":
    import board
    import neopixel

    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    pixel_pin = board.D12

    # The number of NeoPixels
    num_pixels = 24

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    ORDER = neopixel.GRB

    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
    )


class Alarm:

    def __init__(self):
        self.hour = -1
        self.minute = -1

    def set_time(self, h, m):
        self.hour = h
        self.minute = m

    def check(self):
        now = datetime.datetime.now()
        if self.hour == now.hour() and self.minute == now.minute():
            return True
        else:
            return False


def sunrise():
    if OS == "Darwin": return
    for j in range(255):
        pixels.fill((j, j, j))
        pixels.show()
        time.sleep(1)


def sunset():
    if OS == "Darwin": return
    pixels.fill((0, 0, 0))
    pixels.show()


def get_file():
    print("getting URL")
    url = "https://www.srf.ch/feed/podcast/sd/28549e81-c453-4671-92ad-cb28796d06a8.xml"
    feed = feedparser.parse(url)
    link = feed["items"][0]["links"][0]["url"]
    print("getting FILE")
    r = requests.get(link, allow_redirects=True)
    open('podcasts/echo.mp3', 'wb').write(r.content)
    print("converting FILE")
    os.system("ffmpeg -i podcasts/echo.mp3 podcasts/echo.wav")


def play_podcast():
    if OS == "Darwin": return
    os.system("aplay podcasts/echo.wav")


if __name__ == '__main__':
    machine = Alarm()
    machine.set_time(8, 0)
    try:
        while True:
            if machine.check():
                sunrise()
                get_file()
                play_podcast()
                sunset()
            time.sleep(30)
    except KeyboardInterrupt:
        if OS != "Darwin":
            pixels.fill((0, 0, 0))
            pixels.show()
