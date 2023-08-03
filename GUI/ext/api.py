from datetime import datetime

import requests

from GUI.MongoDB.logs import add_log
from GUI.config import load_config
from GUI.models.log import LogStatus, LogService

config = load_config()  # config
users_url = f'{config.links.jewell}/api/users'
courses_url = f'{config.links.jewell}/api/courses'
attendance_url = f'{config.links.jewell}/api/attendance/update'
jewell_token = config.api.jewell


def get_users_from_api() -> (bool, ...):
    return get_data_from_api(users_url)


def get_courses_from_api() -> (bool, ...):
    return get_data_from_api(courses_url)


def get_data_from_api(url: str) -> (bool, ...):
    try:
        r = requests.post(url, json={"token": jewell_token})
        if r.ok:
            res = r.json()
            if res['success']:
                return True, res['data']
        else:
            add_log(LogStatus.ERROR, LogService.GUI, 'Failed to send a request to the server.')
    except Exception as ex:
        add_log(LogStatus.ERROR, LogService.GUI, ex)
    return False, None


def send_attendance(user_id, date, count):
    user_id = str(user_id)
    date = datetime.strftime(date, "%d.%m.%Y %H:%M:%S")
    return requests.post(attendance_url,
                         json={"token": jewell_token,
                               'user_id': user_id,
                               'date': date,
                               'count': count})
