import json

from bson.json_util import loads

from Background.MongoDB.timetables import update_timetable, check_timetable_by_name, add_timetable
from Background.MongoDB.users import users_truncate, add_users
from Background.api import get_users_from_api, get_courses_from_api


def manage_data():
    if not update_users():
        pass
        # todo: add info to message
    if not update_courses_timetable():
        pass
        # todo: add info to message
    # todo: send message


def update_users():
    try:
        status, js = get_users_from_api()
        if status:
            users_truncate()
            users = loads(js)
            add_users(users)
            return True
    except Exception as ex:
        print(ex)
    return False


def update_courses_timetable():
    try:
        status, js = get_courses_from_api()
        if status:
            courses = loads(js)
            days = list()
            for day in range(7):
                days.append(list())
            a = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            for course in courses:
                for k, v in course['timetable'].items():
                    time = json.loads(v)
                    day = days[a.index(k)]
                    if time not in day:
                        time['courses'] = [course['name']]
                        day.append(time)
                    else:
                        for i in day:
                            if i['hours'] == time['hours'] and i['minutes'] == time['minutes']:
                                i['courses'].append(course['name'])
                                break
            if check_timetable_by_name('jewell'):
                update_timetable('jewell', days)
            else:
                add_timetable('jewell', days)
            return True
    except Exception as ex:
        print(ex)
    return False
