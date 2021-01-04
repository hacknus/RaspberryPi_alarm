import feedparser
import os
import requests
import time
from lamp import Lamp
from alarm import Alarm
from audio import Audio


class Machine:

    def __init__(self):
        self.alarms = []
        self.led = Lamp()
        self.audio = Audio()

    def init_alarm(self, hour, minutes, days=[1, 2, 3, 4, 5]):
        self.alarms.append(Alarm(hour, minutes, days))

    def get_file(self):
        print("getting URL")
        url = "https://www.srf.ch/feed/podcast/sd/28549e81-c453-4671-92ad-cb28796d06a8.xml"
        feed = feedparser.parse(url)
        link = feed["items"][0]["links"][0]["url"]
        print("getting FILE")
        r = requests.get(link, allow_redirects=True)
        open('podcasts/echo.mp3', 'wb').write(r.content)
        print("converting FILE")
        os.system("ffmpeg -i podcasts/echo.mp3 podcasts/echo.wav")

    def main(self):
        while True:
            for alarm in self.alarms:
                if alarm.check():
                    self.led.sunrise()
                    self.get_file()
                    self.audio.play_podcast()
                    self.led.turn_off()
            time.sleep(30)


if __name__ == '__main__':
    root = Machine()
    print("setting time")
    root.init_alarm(7 - 1, 10)
    root.led.turn_off()
    try:
        root.main()
    except KeyboardInterrupt:
        print("Aborting at your request.")
    finally:
        root.led.turn_off()
