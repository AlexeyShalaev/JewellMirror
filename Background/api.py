import json

import requests

from Background.MongoDB.logs import add_log
from Background.config import load_config
from Background.models.log import LogStatus, LogService

config = load_config()  # config
users_url = f'{config.links.jewell}/api/users'
courses_url = f'{config.links.jewell}/api/courses'
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
    except Exception as ex:
        add_log(LogStatus.ERROR, LogService.BACKGROUND, ex)
    return False, None
