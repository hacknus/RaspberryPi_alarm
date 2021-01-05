import feedparser
import os
import requests
import pyowm


def get_weather():
    f = open("key.txt", "r")
    api_key = f.read()  # your API Key here as string
    owm = pyowm.OWM(api_key)  # Use API key to get data
    mgr = owm.weather_manager()
    one_call = mgr.one_call(lat=47.36667, lon=8.55)
    temperature = one_call.forecast_daily[0].temperature('celsius').get('day', None)
    feels_temperature = one_call.forecast_daily[0].temperature('celsius').get('feels_like_day', None)
    data = one_call.forecast_daily[0].detailed_status
    return temperature, feels_temperature, data


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
    return link
