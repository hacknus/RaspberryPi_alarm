import os
import platform

OS = platform.system()


class Audio:

    def __init__(self):
        pass

    def say(self, text):
        print(text)
        if OS == "Darwin": return
        os.system("rm temp.wav")
        os.system("rm temp2.wav")
        os.system('pico2wave -w temp.wav "{}"'.format(text))
        os.system("ffmpeg -i temp.wav -ac 2 temp2.wav")
        os.system("aplay temp2.wav")

    def play_song(self, filename):
        if OS == "Darwin": return
        os.system("aplay songs/{}.wav".format(filename))

    def play_podcast(self):
        if OS == "Darwin": return
        os.system("aplay podcasts/echo.wav")
