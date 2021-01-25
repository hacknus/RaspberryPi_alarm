import caldav
from datetime import datetime
from datetime import date
from datetime import timedelta
import pytz

tz = pytz.timezone('CET')


def init():
    f = open("cal_key.txt", "r")
    url = f.readline().replace("\n", "")
    username = f.readline().replace("\n", "")
    password = f.readline().replace("\n", "")
    print(url, username, password)
    client = caldav.DAVClient(url=url, username=username, password=password)
    my_principal = client.principal()
    calendars = my_principal.calendars()
    return calendars


def get_events(calendars, key):
    events = {}
    for c in calendars:
        if c.name == key:
            evs = c.date_search(start=date.today(),
                                end=date.today() + timedelta(days=1),
                                expand=True)
            for ev in evs:
                name = ev.vobject_instance.vevent.summary.value
                dt = ev.vobject_instance.vevent.dtstart.value.replace(tzinfo=pytz.timezone("CET"))
                events[name] = dt
    return events


if __name__ == "__main__":
    cals = init()
    print(get_events(cals, "UZH"))
    print(get_events(cals, "UniBe"))
    print(get_events(cals, "ARIS"))
    print(get_events(cals, "Private"))
    print(get_events(cals, "Birthdays"))
