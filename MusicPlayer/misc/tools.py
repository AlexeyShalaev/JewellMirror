import functools
from datetime import datetime, timedelta

from MusicPlayer.MongoDB.timetables import get_timetable_by_name


def is_free_time():
    # check for shabbat
    now = datetime.now()
    if ((now.weekday() == 4 and now.hour > 12) or
            (now.weekday() == 5 and now.hour < 23)):
        return False

    # check for courses
    r = get_timetable_by_name('jewell')
    if r.success:
        timetable = r.data.days
        for i in timetable[now.weekday()]:
            start_time = now.replace(hour=i['hours'], minute=i['minutes'], second=0)
            end_time = start_time + timedelta(hours=2)
            if start_time < now < end_time:
                return False

    return True


def singleton(cls):
    """Делает класс Одноэлементным классом"""

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance

    wrapper.instance = None
    return wrapper
