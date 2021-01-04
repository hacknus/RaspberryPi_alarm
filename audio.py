import os
import platform

OS = platform.system()


class Audio:

    def __init__(self):
        pass

    def say(self, text):
        if OS == "Darwin": return
        os.system('pico2wave -w temp.wav "{}"'.format(text))
        os.system("aplay temp.wav")

    def play_song(self, filename):
        if OS == "Darwin": return
        os.system("aplay songs/{}.wav".format(filename))

    def play_podcast(self):
        if OS == "Darwin": return
        os.system("aplay podcasts/echo.wav")
