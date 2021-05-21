import caldav
from datetime import date
from datetime import timedelta
import pytz

tz = pytz.timezone('CET')


def init_cals():
    f = open("cal_key.txt", "r")
    url = f.readline().replace("\n", "")
    username = f.readline().replace("\n", "")
    password = f.readline().replace("\n", "")
    client = caldav.DAVClient(url=url, username=username, password=password)
    my_principal = client.principal()
    calendars = my_principal.calendars()
    return calendars


def get_events(calendars, key):
    events = {}
    for c in calendars:
        if c.name == key:
            evs = c.date_search(start=date.today(),
                                end=date.today() + timedelta(days=1) - timedelta(minutes=1))
            for ev in evs:
                name = ev.vobject_instance.vevent.summary.value
                try:
                    dt = ev.vobject_instance.vevent.dtstart.value.replace(tzinfo=pytz.timezone("CET"))
                except TypeError:
                    dt = ev.vobject_instance.vevent.dtstart.value
                events[name] = dt
                print(dt)
    return events


def get_calendar_message():
    cals = init_cals()
    s = ""
    for cal in cals:
        evs = get_events(cals, cal.name)
        num_evs = len(evs)
        if cal.name != "Birthdays":
            if num_evs == 1:
                s += f"You have one event from {cal.name}: "
                for ev in evs.keys():
                    hour = int(evs[ev].strftime("%H")) + int(evs[ev].strftime("%z").replace("+","")[:2])
                    minute = int(evs[ev].strftime("%M"))
                    s += f'{ev} at {hour}:{minute:02}, '
                s = s[:-2]
                s += ",,, "
            elif num_evs > 1:
                s += f"You have {num_evs} events from {cal.name}: "
                for ev in evs.keys():
                    hour = int(evs[ev].strftime("%H")) + int(evs[ev].strftime("%z").replace("+", "")[:2])
                    minute = int(evs[ev].strftime("%M"))
                    s += f'{ev} at {hour}:{minute:02}, '
                s = s[:-2]
                s += ",,, "
        else:
            if len(evs) == 1:
                for ev in evs.keys():
                    s += f"Today is the birthday of {ev.replace('birthday','')},,, "
            elif len(evs) > 1:
                s += "Today is the birthday of"
                for ev in evs.keys():
                    s += f" {ev} and "
                s = s[:-4]
                s += ",,, "
    if s == "":
        s = "You have no events scheduled for today,,, "
    return s


if __name__ == "__main__":
    print(get_calendar_message())
