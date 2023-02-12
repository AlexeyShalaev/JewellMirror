from datetime import datetime

import requests


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
        return "Янв" if short else "января"
    elif m == 2:
        return "Фев" if short else "февраля"
    elif m == 3:
        return "Март" if short else "марта"
    elif m == 4:
        return "Апр" if short else "апреля"
    elif m == 5:
        return "Май" if short else "мая"
    elif m == 6:
        return "Июнь" if short else "июня"
    elif m == 7:
        return "Июль" if short else "июля"
    elif m == 8:
        return "Авг" if short else "августа"
    elif m == 9:
        return "Сент" if short else "сентября"
    elif m == 10:
        return "Окт" if short else "октября"
    elif m == 11:
        return "Нояб" if short else "ноября"
    elif m == 12:
        return "Дек" if short else "декабря"
    else:
        return str(m)
