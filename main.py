import pytz
import datetime
import time
import json
from lamp import Lamp
from alarm import Alarm
from audio import Audio
from webhelper import get_file, get_weather
import platform

tz = pytz.timezone('Europe/Zurich')
OS = platform.system()


class Machine:

    def __init__(self):
        self.alarms = []
        self.alarms_dict = {"alarms": []}
        self.led = Lamp()
        self.audio = Audio()

    def init_alarm(self, hour, minutes, days=[1, 2, 3, 4, 5]):
        self.alarms.append(Alarm(hour, minutes, days))
        self.dump_alarms()

    def dump_alarms(self):
        all_alarms = []
        for a in self.alarms:
            d = {
                "hour": a.hour,
                "minute": a.minute,
                "days": a.days,
            }
            all_alarms.append(d)
        self.alarms_dict["alarms"] = all_alarms
        with open('alarms.json', 'w') as f:
            json.dump(self.alarms_dict, f)

    def load_alarms(self):
        with open('alarms.json', 'r') as f:
            self.alarms_dict = json.load(f)
        for i in range(len(self.alarms)):
            self.alarms[i].hour = self.alarms_dict["alarms"][i]["hour"]
            self.alarms[i].minute = self.alarms_dict["alarms"][i]["minute"]
            self.alarms[i].days = self.alarms_dict["alarms"][i]["days"]

    def wake_up(self):
        self.led.sunrise()
        now = datetime.datetime.now().replace(tzinfo=tz)
        h = now.hour
        m = now.minute
        t = "{0:02}:{1:02}".format(h, m)
        day = now.day
        months = ["January", "February", "Mars", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        month = months[now.month - 1]
        temp, temp_feels, weather = get_weather()
        forecast = "Good morning Linus, It is {} on the {}. of {}. The temperature outside is {} and feels like {} " \
                   "degrees centigrade and the weather status is {}. " \
                   "Stand by for the news.".format(t, day, month, temp, temp_feels, weather)
        self.audio.say(forecast)
        get_file()
        self.audio.play_podcast()
        self.led.turn_off()

    def main(self):
        while True:
            self.load_alarms()
            print(datetime.datetime.now().replace(tzinfo=tz))
            for alarm in self.alarms:
                if alarm.check() or OS == "Darwin":
                    print("waking up")
                    self.wake_up()
            time.sleep(30)


if __name__ == '__main__':
    root = Machine()
    print("setting time")
    root.init_alarm(23, 48)
    root.led.turn_off()
    try:
        root.main()
    except KeyboardInterrupt:
        print("Aborting at your request.")
    finally:
        root.led.turn_off()
