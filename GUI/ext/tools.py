import functools
from datetime import datetime, timedelta

import requests

from GUI.MongoDB.timetables import get_timetable_by_name


def shabbat(geo_name_id: int = 524901) -> dict:
    # https://www.hebcal.com/home/197/shabbat-times-rest-api
    url = f'https://www.hebcal.com/shabbat?cfg=json&geonameid={geo_name_id}'
    res = {"candle": "", "havdalah": ""}
    try:
        request = requests.get(url)
        if request.ok:
            for i in request.json()['items']:
                try:
                    title = i['title']
                    date = i['date']
                    if "T" in date:
                        if "+" in date:
                            date = datetime.strptime(date[:date.index('+')], '%Y-%m-%dT%H:%M:%S')
                        else:
                            date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
                    else:
                        date = datetime.strptime(date, '%Y-%m-%d')
                    if title.startswith('Candle'):
                        res[
                            'candle'] = f'{date.day} {get_month(date.month)} в {date.hour}:{"0" * (2 - len(str(date.minute))) + str(date.minute)}'
                    elif title.startswith('Havdalah'):
                        res[
                            'havdalah'] = f'{date.day} {get_month(date.month)} в {date.hour}:{"0" * (2 - len(str(date.minute))) + str(date.minute)}'
                except:
                    pass
    except:
        pass
    return res


def get_month(m: int, short: bool = True) -> str:
    if m == 1:
        return "Янв" if short else "Января"
    elif m == 2:
        return "Фев" if short else "Февраля"
    elif m == 3:
        return "Март" if short else "Марта"
    elif m == 4:
        return "Апр" if short else "Апреля"
    elif m == 5:
        return "Май" if short else "Мая"
    elif m == 6:
        return "Июнь" if short else "Июня"
    elif m == 7:
        return "Июль" if short else "Июля"
    elif m == 8:
        return "Авг" if short else "Августа"
    elif m == 9:
        return "Сент" if short else "Сентября"
    elif m == 10:
        return "Окт" if short else "Октября"
    elif m == 11:
        return "Нояб" if short else "Ноября"
    elif m == 12:
        return "Дек" if short else "Декабря"
    else:
        return str(m)


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
