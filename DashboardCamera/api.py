from datetime import datetime

import requests

from DashboardCamera.MongoDB.logs import add_log
from DashboardCamera.config import load_config
from DashboardCamera.models.log import LogStatus, LogService

config = load_config()  # config
attendance_visit_url = f'{config.links.jewell}/api/attendance/visit'
qr_attendance_url = f'{config.links.jewell}/api/attendance/qrcode'
say_text_url = f'{config.links.music_player}/api/speech/say'

jewell_token = config.api.jewell
mp_token = config.api.music_player


def send_attendance_visit(user_id, date):
    date = datetime.strftime(date, "%d.%m.%Y %H:%M:%S")
    return requests.post(attendance_visit_url,
                         json={"token": jewell_token,
                               'user_id': str(user_id),
                               'date': date})


def get_qr_visits_uri():
    r = requests.post(qr_attendance_url, json={"token": jewell_token})
    if r.ok:
        res = r.json()
        if res['success']:
            return config.links.jewell + res['uri']
    else:
        add_log(LogStatus.ERROR, LogService.CAMERA, 'Не удалось получить QR код для посещаемости')
    return None


def say_text(text):
    try:
        requests.post(say_text_url,
                      json={"token": mp_token,
                            'text': text},
                      timeout=1)
    except:
        pass
