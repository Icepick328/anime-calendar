from ics import Calendar, Event
from datetime import datetime
import pytz
from config import TIMEZONE

tz = pytz.timezone(TIMEZONE)

def build_event(title, episode, airing_at, description, url):
    e = Event()

    dt = datetime.fromtimestamp(airing_at, tz)

    e.name = f"{title} - Episode {episode}"
    e.begin = dt
    e.description = description
    e.url = url

    return e


def create_calendar(events):
    cal = Calendar()
    for e in events:
        cal.events.add(e)
    return cal
