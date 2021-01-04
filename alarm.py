import datetime


class Alarm:

    def __init__(self, hour, minutes, days):
        self.hour = hour
        self.minute = minutes
        self.days = days

    def set_time(self, h, m, d):
        self.hour = h
        self.minute = m
        self.days = d

    def check(self):
        now = datetime.datetime.now()
        if self.hour == now.hour and self.minute == now.minute:
            return True
        else:
            return False