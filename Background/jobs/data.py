import json

from Background.MongoDB.timetables import update_timetable
from Background.MongoDB.users import truncate, add_users


def manage_data():
    if not update_users():
        pass
        # add info to message
    if not update_courses_timetable():
        pass
        # add info to message
    # send message


def update_users():
    try:
        # обновляем данные о поль-ах, чтобы вдруг кто-тьо обновил фото лица
        users = [...]  # todo request to jms
        truncate()
        add_users(users)
        return True
    except:
        return False


def update_courses_timetable():
    try:
        courses = [
            {"timetable": {
                "sunday": "{\"hours\": 13, \"minutes\": 0}"
            }},
            {"timetable": {
                "sunday": "{\"hours\": 15, \"minutes\": 0}"
            }},
            {"timetable": {
                "sunday": "{\"hours\": 15, \"minutes\": 0}"
            }},
            {"timetable": {
                "sunday": "{\"hours\": 17, \"minutes\": 0}"
            }},
            {"timetable": {
                "sunday": "{\"hours\": 17, \"minutes\": 0}"
            }},
            {"timetable": {
                "monday": "{\"hours\": 19, \"minutes\": 0}"
            }},
            {"timetable": {
                "monday": "{\"hours\": 20, \"minutes\": 0}"
            }},
            {"timetable": {
                "tuesday": "{\"hours\": 19, \"minutes\": 0}",
            }},
            {"timetable": {
                "wednesday": "{\"hours\": 19, \"minutes\": 0}",
            }},
            {"timetable": {
                "wednesday": "{\"hours\": 20, \"minutes\": 0}"
            }},
            {"timetable": {
                "thursday": "{\"hours\": 19, \"minutes\": 0}"
            }},
            {"timetable": {
                "thursday": "{\"hours\": 19, \"minutes\": 0}"
            }},
            {"timetable": {
                "tuesday": "{\"hours\": 19, \"minutes\": 30}",
                "thursday": "{\"hours\": 19, \"minutes\": 30}",
                "sunday": "{\"hours\": 19, \"minutes\": 30}"
            }},
            {"timetable": {
                "tuesday": "{\"hours\": 19, \"minutes\": 0}",
                "thursday": "{\"hours\": 19, \"minutes\": 0}",
                "sunday": "{\"hours\": 19, \"minutes\": 0}"
            }},
        ]  # todo request to jms
        days = list()
        for day in range(7):
            days.append(list())
        a = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for course in courses:
            for k, v in course['timetable'].items():
                time = json.loads(v)
                day = days[a.index(k)]
                if time not in day:
                    time['courses'] = course['name']
                    day.append(time)
                else:
                    for i in day:
                        if i['hours'] == time['hours'] and i['minutes'] == time['minutes']:
                            i['courses'] += f"/{course['name']}"
                            break
        update_timetable('jewell', days)
        """
                                        timetable = [[{'hours': 19, 'minutes': 0, 'courses': '1/2'}, {'hours': 20, 'minutes': 0}],
                                                     [{'hours': 19, 'minutes': 0}, {'hours': 19, 'minutes': 30}],
                                                     [{'hours': 19, 'minutes': 0}, {'hours': 20, 'minutes': 0}],
                                                     [{'hours': 19, 'minutes': 0}, {'hours': 19, 'minutes': 30}],
                                                     [],
                                                     [],
                                                     [{'hours': 13, 'minutes': 0}, {'hours': 15, 'minutes': 0},
                                                      {'hours': 17, 'minutes': 0},
                                                      {'hours': 19, 'minutes': 30}, {'hours': 19, 'minutes': 0}]]
                                          """

        return True
    except:
        return False
