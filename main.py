import feedparser
import os
import requests

def get_file():
    url = "https://www.srf.ch/feed/podcast/sd/28549e81-c453-4671-92ad-cb28796d06a8.xml"
    feed = feedparser.parse(url)
    link = feed["items"][0]["links"][0]["url"]
    r = requests.get(link, allow_redirects=True)
    open('podcasts/echo.mp3', 'wb').write(r.content)


if __name__ == '__main__':


